-- Tracking propio de kinedu.com (visitas, únicos, CTAs, referrers, idiomas, blog, búsquedas, A/B, crawlers)
-- en Supabase, en lugar de Upstash Redis (que topaba los 500K comandos/mes del plan gratis).
--
-- Se corre UNA vez en el SQL Editor del proyecto de Supabase (y de nuevo solo si cambia).
-- Después, en Vercel (proyecto kinedu-landing) van dos variables de entorno:
--   SUPABASE_URL               = https://<ref>.supabase.co
--   SUPABASE_SERVICE_ROLE_KEY  = la service-role key del proyecto (solo servidor; nunca al navegador)
-- Con esas dos presentes, /api/track y /api/stats usan Supabase; sin ellas siguen con Upstash.
--
-- Modelo: un contador por (día, tipo, clave). Una visita = 4 a 6 filas incrementadas en UNA llamada (rpc web_track).
-- Únicos por día = hash IP+UA+fecha en web_uv (misma definición que antes).

create table if not exists public.web_daily (
  date date not null,
  kind text not null,   -- 'pv' | 'conv' | 'ref' | 'lang' | 'cta' | 'ab_view' | 'ab_cta' | 'crawl' | 'cat' | 'catconv' | 'search' | '_uv' (importado)
  key  text not null,   -- página, dominio, idioma, etiqueta del CTA, categoría, término...
  n    integer not null default 0,
  primary key (date, kind, key)
);
create index if not exists web_daily_kind_idx on public.web_daily (kind, date);

create table if not exists public.web_uv (
  date date not null,
  vid  text not null,   -- sha256(ip + user-agent + fecha), 16 hex
  primary key (date, vid)
);

-- Cerradas con RLS y sin policies: solo el servidor (service_role) entra.
alter table public.web_daily enable row level security;
alter table public.web_uv    enable row level security;
grant usage on schema public to service_role;
grant select, insert, update on public.web_daily to service_role;
grant select, insert         on public.web_uv    to service_role;

-- Una visita/evento: incrementa varios contadores y registra el visitante único, en una sola llamada.
-- p_items = [{"k":"pv","key":"/blog/x"},{"k":"lang","key":"es"},...]
create or replace function public.web_track(p_date date, p_vid text, p_items jsonb)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.web_daily (date, kind, key, n)
  select p_date, i->>'k', left(i->>'key', 200), 1
  from jsonb_array_elements(p_items) i
  where coalesce(i->>'k','') <> '' and coalesce(i->>'key','') <> ''
  on conflict (date, kind, key) do update set n = public.web_daily.n + 1;

  if p_vid is not null and p_vid <> '' then
    insert into public.web_uv (date, vid) values (p_date, p_vid) on conflict do nothing;
  end if;
end;
$$;

-- Importación de histórico (p. ej. desde Upstash): fija valores absolutos, no incrementa.
-- p_rows = [{"date":"2026-09-01","k":"pv","key":"/","n":123}, ...]  ('_uv' con key '_' = únicos del día ya contados)
create or replace function public.web_import(p_rows jsonb)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare c integer;
begin
  insert into public.web_daily (date, kind, key, n)
  select (r->>'date')::date, r->>'k', left(r->>'key', 200), (r->>'n')::integer
  from jsonb_array_elements(p_rows) r
  on conflict (date, kind, key) do update set n = excluded.n;
  get diagnostics c = row_count;
  return c;
end;
$$;

-- Lectura para /analytics: todos los contadores de un rango de días, agrupados por día y tipo, más los totales históricos.
-- {"days":[{"date":"2026-09-22","uv":123,"counters":{"pv":{"/":50,...},"lang":{...}}}], "totals":{"pv":..., "conv":...}}
create or replace function public.web_stats(p_from date, p_to date)
returns jsonb
language sql
security definer
set search_path = public
stable
as $$
  select jsonb_build_object(
    'days', coalesce((
      select jsonb_agg(jsonb_build_object(
               'date', x.date,
               'uv', greatest(
                       (select count(*) from public.web_uv u where u.date = x.date),
                       coalesce((select n from public.web_daily w where w.date = x.date and w.kind = '_uv' and w.key = '_'), 0)),
               'counters', coalesce((
                 select jsonb_object_agg(s.kind, s.m)
                 from (select w.kind, jsonb_object_agg(w.key, w.n) m
                       from public.web_daily w where w.date = x.date and w.kind <> '_uv' group by w.kind) s), '{}'::jsonb)
             ) order by x.date)
      from (select distinct date from public.web_daily where date between p_from and p_to
            union select distinct date from public.web_uv where date between p_from and p_to) x
    ), '[]'::jsonb),
    'totals', (select jsonb_build_object(
                 'pv',   coalesce(sum(n) filter (where kind = 'pv'), 0),
                 'conv', coalesce(sum(n) filter (where kind = 'conv'), 0))
               from public.web_daily)
  );
$$;

revoke all on function public.web_track(date, text, jsonb) from public;
revoke all on function public.web_import(jsonb) from public;
revoke all on function public.web_stats(date, date) from public;
grant execute on function public.web_track(date, text, jsonb) to service_role;
grant execute on function public.web_import(jsonb) to service_role;
grant execute on function public.web_stats(date, date) to service_role;

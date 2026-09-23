// Copia el histórico del tracking de Upstash Redis a Supabase (rpc web_import), día por día.
// Uso: KV_REST_API_URL=... KV_REST_API_TOKEN=... SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... \
//      node scripts/analytics/upstash-to-supabase.js 2026-08-01 2026-09-22
// Requiere que Upstash tenga cuota (cada día cuesta 12 comandos). Los únicos por día se importan como
// contador '_uv' (los hashes de visitante no se pueden reconstruir desde un HyperLogLog).
const FIELDS = ['pv', 'conv', 'ref', 'lang', 'cta', 'ab_view', 'ab_cta', 'crawl', 'cat', 'catconv', 'search'];
const [from, to] = process.argv.slice(2);
if (!from || !to) { console.error('uso: node upstash-to-supabase.js YYYY-MM-DD YYYY-MM-DD'); process.exit(1); }
const KV = process.env.KV_REST_API_URL, KT = process.env.KV_REST_API_TOKEN, SU = process.env.SUPABASE_URL, SK = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!KV || !KT || !SU || !SK) { console.error('faltan variables de entorno'); process.exit(1); }

async function kv(cmds) {
  const r = await fetch(`${KV}/pipeline`, { method: 'POST', headers: { Authorization: `Bearer ${KT}`, 'Content-Type': 'application/json' }, body: JSON.stringify(cmds) });
  return r.json();
}
async function sb(fn, args) {
  const r = await fetch(`${SU.replace(/\/$/, '')}/rest/v1/rpc/${fn}`, { method: 'POST', headers: { apikey: SK, Authorization: `Bearer ${SK}`, 'Content-Type': 'application/json' }, body: JSON.stringify(args) });
  if (!r.ok) throw new Error(`${fn} ${r.status}: ${await r.text()}`);
  return r.json();
}
(async () => {
  const d = new Date(from + 'T00:00:00Z'); const end = new Date(to + 'T00:00:00Z');
  let days = 0, rows = 0;
  for (; d <= end; d.setUTCDate(d.getUTCDate() + 1)) {
    const date = d.toISOString().slice(0, 10);
    const res = await kv([...FIELDS.map((f) => ['HGETALL', `analytics:${f}:${date}`]), ['PFCOUNT', `analytics:uv:${date}`]]);
    const bad = res.find((x) => x && x.error); if (bad) { console.error(date, 'upstash:', bad.error); process.exit(2); }
    const out = [];
    FIELDS.forEach((f, i) => { const arr = (res[i] && res[i].result) || []; for (let j = 0; j < arr.length; j += 2) out.push({ date, k: f, key: arr[j], n: parseInt(arr[j + 1]) || 0 }); });
    const uv = parseInt(res[FIELDS.length] && res[FIELDS.length].result) || 0;
    if (uv) out.push({ date, k: '_uv', key: '_', n: uv });
    if (out.length) { const n = await sb('web_import', { p_rows: out }); rows += n; }
    days++; console.log(date, out.length, 'filas');
  }
  console.log(`listo: ${days} días, ${rows} filas importadas`);
})().catch((e) => { console.error(e.message); process.exit(3); });

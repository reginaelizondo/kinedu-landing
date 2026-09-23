// Almacén del tracking propio: Supabase (Postgres) si están sus variables, si no Upstash Redis (legado).
// Supabase: tablas web_daily / web_uv y RPCs web_track / web_stats / web_import (supabase/analytics.sql).
function supabase() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return null;
  const rpc = async (fn, args) => {
    const r = await fetch(`${url.replace(/\/$/, '')}/rest/v1/rpc/${fn}`, {
      method: 'POST',
      headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', Prefer: 'return=representation' },
      body: JSON.stringify(args),
    });
    const text = await r.text();
    if (!r.ok) throw new Error(`supabase ${fn} ${r.status}: ${text.slice(0, 300)}`);
    return text ? JSON.parse(text) : null;
  };
  return { kind: 'supabase', rpc };
}

function upstash() {
  const url = process.env.KV_REST_API_URL;
  const token = process.env.KV_REST_API_TOKEN;
  if (!url || !token) return null;
  const pipeline = async (cmds) => {
    const r = await fetch(`${url}/pipeline`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(cmds),
    });
    return r.json();
  };
  return { kind: 'upstash', pipeline };
}

module.exports = { supabase, upstash };

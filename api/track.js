const crypto = require('crypto');
const { supabase, upstash } = require('./_store');

// Filtro anti-bots: crawlers, headless y clientes programáticos no cuentan como visitas humanas.
// (Los buscadores ejecutan JS y disparan el beacon; sin esto inflan las vistas tras cada deploy.)
const BOT_RE = /bot\b|bot\/|crawl|spider|slurp|bingpreview|googlebot|bingbot|yandex|baidu|duckduck|applebot|facebookexternalhit|facebot|twitterbot|linkedinbot|whatsapp|telegram|slack|discord|embedly|pinterest|redditbot|ahrefs|semrush|mj12|dotbot|petalbot|bytespider|gptbot|ccbot|claudebot|anthropic|perplexity|amazonbot|headless|phantom|puppeteer|playwright|selenium|lighthouse|pagespeed|gtmetrix|pingdom|uptimerobot|curl|wget|python-requests|python-httpx|axios|node-fetch|go-http-client|java\/|okhttp|libwww|httpclient|scrapy|monitor/i;

// Traduce un evento del beacon a contadores (kind, key). Misma semántica que las claves analytics:* de Redis.
function itemsFor(body, date) {
  const page = body.page || '/';
  const event = body.event || 'pageview';
  const lang = body.lang || 'en';
  const cat = (body.cat || '').toString().trim().slice(0, 40);
  const items = [];
  const add = (k, key) => items.push({ k, key: String(key).slice(0, 200) });

  if (event === 'search') {
    const q = (body.q || '').toString().toLowerCase().trim().replace(/\s+/g, ' ').slice(0, 40);
    if (q.length >= 2) add('search', `${lang}|${q}`);
    return { items, countsAsVisit: false };
  }
  if (event === 'ab_view') {
    if (body.variant) add('ab_view', `${page}|${body.variant}`);
    return { items, countsAsVisit: false };
  }
  // Clic de un A/B que NO es conversión del sitio (p. ej. tocar un ítem del menú móvil):
  // suma a ab_cta para abSummary sin tocar conversiones ni vistas. Antes (20-oct) el menú
  // mandaba menu_open/menu_click, que no existían aquí y caían como pageview.
  if (event === 'ab_cta') {
    if (body.variant) add('ab_cta', `${page}|${body.variant}`);
    return { items, countsAsVisit: false };
  }

  add('pv', page); add('lang', lang);
  if (cat) add('cat', cat);
  if (event === 'conversion') {
    add('conv', page); add('cta', body.cta || 'unknown');
    if (cat) add('catconv', cat);
    if (body.variant) add('ab_cta', `${page}|${body.variant}`);
  }
  if (body.referrer) {
    try { const h = new URL(body.referrer).hostname; if (h) add('ref', h); } catch (e) { /* referrer inválido */ }
  }
  // Campañas (18-nov-2026): una vista que llega con utm_source (correos, anuncios) se cuenta aparte en
  // 'utm' con clave source|campaign|page, para ver en /analytics cuántos entraron a /gift desde un correo.
  // Solo en pageview (no en conversion, que también suma pv) para contar una vez por llegada.
  if (event === 'pageview' && body._utm && body._utm.source) add('utm', `${body._utm.source}|${body._utm.campaign || ''}|${page}`);
  return { items, countsAsVisit: true };
}

// utm_source/utm_campaign de la URL de la página. Los beacons no mandan la query, pero sendBeacon
// a /api/track es same-origin y el navegador manda el Referer completo (con query); también se
// aceptan body.utm_source / body.utm_campaign si una página los manda explícitos.
function utmOf(body, referer) {
  const clean = (v) => (v || '').toString().toLowerCase().trim().replace(/[^a-z0-9_.\-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40);
  let source = clean(body.utm_source), campaign = clean(body.utm_campaign);
  if (!source && referer) {
    try { const u = new URL(referer); source = clean(u.searchParams.get('utm_source')); if (!campaign) campaign = clean(u.searchParams.get('utm_campaign')); } catch (e) { /* referer inválido */ }
  }
  return source ? { source, campaign } : null;
}

// Filtro de bucles (decisión de Paola, "referrer", 25-nov-2026): una vista (pageview) cuyo referrer es
// la misma página en kinedu.com es la página recargándose a sí misma (los picos del home del 10, 14, 16
// y 20-nov traían ~48% de referrer www.kinedu.com con visitantes únicos planos). Se descarta.
// Conversiones, clics y A/B no pasan por aquí. Costo asumido: se pierde la recarga legítima del mismo URL.
function isSelfReferral(body) {
  if ((body.event || 'pageview') !== 'pageview' || !body.referrer) return false;
  try {
    const u = new URL(body.referrer);
    if (!/(^|\.)kinedu\.com$/i.test(u.hostname)) return false;
    const norm = (p) => (p || '/').replace(/\/index\.html$/i, '/').replace(/\/+$/, '') || '/';
    return norm(u.pathname) === norm(body.page);
  } catch (e) { return false; }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const db = supabase() || upstash();
  if (!db) return res.status(200).json({ ok: true, note: 'store not configured' });

  try {
    let body = req.body;
    if (typeof body === 'string') body = JSON.parse(body);
    body = body || {};
    const date = new Date().toISOString().slice(0, 10);
    const ip = (req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || '0.0.0.0').split(',')[0].trim();
    const ua = req.headers['user-agent'] || '';

    if (!ua || BOT_RE.test(ua)) {
      // Actividad de buscadores, contada aparte (señal SEO), nunca mezclada con vistas humanas.
      const cm = ua && ua.match(/(googlebot|bingbot|applebot|duckduckbot|yandex)/i);
      if (cm) {
        try {
          if (db.kind === 'supabase') await db.rpc('web_track', { p_date: date, p_vid: null, p_items: [{ k: 'crawl', key: cm[1].toLowerCase() }] });
          else await db.pipeline([['HINCRBY', `analytics:crawl:${date}`, cm[1].toLowerCase(), 1]]);
        } catch (e) { console.error('Track crawl error:', e.message); }
      }
      return res.status(200).json({ ok: true, skipped: 'bot' });
    }

    if (isSelfReferral(body)) return res.status(200).json({ ok: true, skipped: 'self-referrer' });

    body._utm = utmOf(body, req.headers.referer || req.headers.referrer);
    const { items, countsAsVisit } = itemsFor(body, date);
    if (!items.length) return res.status(200).json({ ok: true, skipped: 'empty' });
    const vid = countsAsVisit ? crypto.createHash('sha256').update(ip + ua + date).digest('hex').slice(0, 16) : null;

    if (db.kind === 'supabase') {
      await db.rpc('web_track', { p_date: date, p_vid: vid, p_items: items });
    } else {
      const pipeline = items.map(({ k, key }) => (k === 'pv' ? ['HINCRBY', `analytics:pv:${date}`, key, 1] : ['HINCRBY', `analytics:${k}:${date}`, key, 1]));
      if (vid) pipeline.push(['PFADD', `analytics:uv:${date}`, vid], ['INCR', 'analytics:total:pv']);
      if (items.some((i) => i.k === 'conv')) pipeline.push(['INCR', 'analytics:total:conv']);
      const j = await db.pipeline(pipeline);
      const bad = !Array.isArray(j) ? j : j.find((x) => x && x.error);
      if (bad) console.error('Track KV error:', JSON.stringify(bad).slice(0, 300));
    }
    res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Track error:', err && err.message);
    res.status(200).json({ ok: true });
  }
};
module.exports.itemsFor = itemsFor;
module.exports.utmOf = utmOf;
module.exports.isSelfReferral = isSelfReferral;

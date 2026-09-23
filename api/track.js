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
  return { items, countsAsVisit: true };
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

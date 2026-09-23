// Agrega los contadores diarios de Redis (Upstash) para /analytics.
//
// Coste en comandos (cada comando de un pipeline cuenta contra la cuota mensual de Upstash):
//   - Un día ya cerrado se guarda resumido en `analytics:day:<fecha>` la primera vez que se pide;
//     después cuesta 1 GET en vez de 12 HGETALL/PFCOUNT. Solo el día de hoy se lee "en crudo".
//   - Con 14 días: ~13 GET + 12 (hoy) + 2 totales ≈ 27 comandos (antes 170); con 90: ~105 (antes 1,082).
//   - Si Upstash devuelve "max requests limit exceeded", respondemos 503 {error:'kv_quota'} para que el
//     dashboard lo diga en vez de mostrar ceros.
const FIELDS = ['pv', 'uv', 'conv', 'ref', 'lang', 'cta', 'ab_view', 'ab_cta', 'crawl', 'cat', 'catconv', 'search'];
const FIELDS_PER_DAY = FIELDS.length;
const DAY_CACHE_TTL = 400 * 86400; // segundos; un año largo

function parseHash(result) {
  const hash = {};
  const arr = (result && result.result) || [];
  for (let j = 0; j < arr.length; j += 2) hash[arr[j]] = parseInt(arr[j + 1]) || 0;
  return hash;
}

function dayFromResults(results, offset, date) {
  const r = (k) => results[offset + FIELDS.indexOf(k)];
  const pages = parseHash(r('pv'));
  const conversions = parseHash(r('conv'));
  let totalPV = 0; for (const k in pages) totalPV += pages[k];
  let totalConv = 0; for (const k in conversions) totalConv += conversions[k];
  return {
    date,
    pageViews: totalPV,
    uniqueVisitors: (r('uv') && r('uv').result) || 0,
    conversions: totalConv,
    convByPage: conversions,
    pages,
    referrers: parseHash(r('ref')),
    languages: parseHash(r('lang')),
    ctaClicks: parseHash(r('cta')),
    abViews: parseHash(r('ab_view')),
    abCta: parseHash(r('ab_cta')),
    crawlers: parseHash(r('crawl')),
    cats: parseHash(r('cat')),
    catConv: parseHash(r('catconv')),
    searches: parseHash(r('search')),
  };
}

function quotaError(results) {
  if (!Array.isArray(results)) return (results && results.error) || 'KV error';
  for (const x of results) if (x && x.error && /max requests limit/i.test(x.error)) return x.error;
  return null;
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const password = req.query.password || req.headers['x-analytics-password'];
  const ANALYTICS_PASSWORD = process.env.ANALYTICS_PASSWORD;
  if (!ANALYTICS_PASSWORD || password !== ANALYTICS_PASSWORD) return res.status(401).json({ error: 'Unauthorized' });

  const KV_URL = process.env.KV_REST_API_URL;
  const KV_TOKEN = process.env.KV_REST_API_TOKEN;
  if (!KV_URL || !KV_TOKEN) return res.status(500).json({ error: 'KV not configured' });

  const kv = async (cmds) => {
    const r = await fetch(`${KV_URL}/pipeline`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KV_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(cmds),
    });
    return r.json();
  };

  try {
    const days = Math.min(365, Math.max(1, parseInt(req.query.days) || 30));
    const dates = [];
    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      dates.push(d.toISOString().slice(0, 10));
    }
    const today = new Date().toISOString().slice(0, 10);

    // 1) días cerrados: intentar el resumen cacheado (1 comando por día)
    const past = dates.filter((d) => d < today);
    const cached = {};
    if (past.length) {
      const r = await kv(past.map((d) => ['GET', `analytics:day:${d}`]));
      const qe = quotaError(r);
      if (qe) return res.status(503).json({ error: 'kv_quota', message: qe });
      past.forEach((d, i) => {
        const v = r[i] && r[i].result;
        if (v) { try { cached[d] = JSON.parse(v); } catch (e) { /* recalcula abajo */ } }
      });
    }

    // 2) hoy + los días sin resumen: lectura en crudo
    const need = dates.filter((d) => !cached[d]);
    const pipeline = [];
    for (const date of need) for (const f of FIELDS) pipeline.push(f === 'uv' ? ['PFCOUNT', `analytics:uv:${date}`] : ['HGETALL', `analytics:${f}:${date}`]);
    pipeline.push(['GET', 'analytics:total:pv']);
    pipeline.push(['GET', 'analytics:total:conv']);
    const results = await kv(pipeline);
    const qe = quotaError(results);
    if (qe) return res.status(503).json({ error: 'kv_quota', message: qe });

    const fresh = {};
    need.forEach((date, i) => { fresh[date] = dayFromResults(results, i * FIELDS_PER_DAY, date); });
    const totalPV = parseInt((results[need.length * FIELDS_PER_DAY] || {}).result) || 0;
    const totalConv = parseInt((results[need.length * FIELDS_PER_DAY + 1] || {}).result) || 0;

    // 3) guardar el resumen de los días cerrados que se acaban de calcular (solo la primera vez)
    const toCache = need.filter((d) => d < today);
    if (toCache.length) {
      try { await kv(toCache.map((d) => ['SET', `analytics:day:${d}`, JSON.stringify(fresh[d]), 'EX', DAY_CACHE_TTL])); } catch (e) { /* best effort */ }
    }

    const daily = dates.map((d) => cached[d] || fresh[d]);

    // Agregados
    const topPages = {}, topReferrers = {}, topLanguages = {}, topCTAs = {}, abViews = {}, abCta = {}, topCats = {}, topCatConv = {}, topSearches = {}, crawlTotals = {};
    let sumUV = 0, sumPV = 0, sumConv = 0;
    const add = (acc, obj) => { for (const k in obj) acc[k] = (acc[k] || 0) + obj[k]; };
    for (const day of daily) {
      sumPV += day.pageViews; sumUV += day.uniqueVisitors; sumConv += day.conversions;
      add(topPages, day.pages); add(topReferrers, day.referrers); add(topLanguages, day.languages); add(topCTAs, day.ctaClicks);
      add(abViews, day.abViews); add(abCta, day.abCta); add(topCats, day.cats); add(topCatConv, day.catConv); add(topSearches, day.searches); add(crawlTotals, day.crawlers);
    }

    const abSummary = {};
    const langOf = (page) => (page.includes('-en') ? 'en' : page.includes('-es') ? 'es' : page.includes('-pt') ? 'pt' : 'en');
    for (const [key, count] of Object.entries(abViews)) {
      const [page, variant] = key.split('|'); const lang = langOf(page);
      if (!abSummary[lang]) abSummary[lang] = { a: { views: 0, cta: 0 }, b: { views: 0, cta: 0 } };
      if (variant === 'a' || variant === 'b') abSummary[lang][variant].views += count;
    }
    for (const [key, count] of Object.entries(abCta)) {
      const [page, variant] = key.split('|'); const lang = langOf(page);
      if (!abSummary[lang]) abSummary[lang] = { a: { views: 0, cta: 0 }, b: { views: 0, cta: 0 } };
      if (variant === 'a' || variant === 'b') abSummary[lang][variant].cta += count;
    }

    const sorted = (o) => Object.entries(o).sort((a, b) => b[1] - a[1]);
    res.setHeader('Cache-Control', 's-maxage=120, stale-while-revalidate=300');
    res.status(200).json({
      period: { days, from: dates[0], to: dates[dates.length - 1] },
      summary: {
        pageViews: sumPV, uniqueVisitors: sumUV, conversions: sumConv,
        conversionRate: sumUV > 0 ? ((sumConv / sumUV) * 100).toFixed(2) : '0.00',
      },
      daily,
      topPages: sorted(topPages), topReferrers: sorted(topReferrers), topLanguages: sorted(topLanguages), topCTAs: sorted(topCTAs),
      abSummary,
      topCategories: sorted(topCats), topCategoryConv: sorted(topCatConv), topSearches: sorted(topSearches).slice(0, 100),
      crawlTotals,
      allTimeTotals: { pageViews: totalPV, conversions: totalConv },
      cache: { cachedDays: Object.keys(cached).length, rawDays: need.length },
    });
  } catch (err) {
    console.error('Stats error:', err);
    res.status(500).json({ error: 'Failed to fetch analytics' });
  }
};

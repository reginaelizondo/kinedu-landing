// Agregados del tracking propio para /analytics. Mismo JSON de siempre (daily[], summary, top*, abSummary...),
// leído de Supabase (una llamada: rpc web_stats) o, si no está configurado, de Upstash Redis con un resumen
// cacheado por día (analytics:day:<fecha>) para gastar ~1 comando por día cerrado en vez de 12.
const { supabase, upstash } = require('./_store');

const FIELDS = ['pv', 'uv', 'conv', 'ref', 'lang', 'cta', 'ab_view', 'ab_cta', 'crawl', 'cat', 'catconv', 'search'];
const DAY_CACHE_TTL = 400 * 86400;

function emptyDay(date) {
  return { date, pageViews: 0, uniqueVisitors: 0, conversions: 0, convByPage: {}, pages: {}, referrers: {}, languages: {}, ctaClicks: {}, abViews: {}, abCta: {}, crawlers: {}, cats: {}, catConv: {}, searches: {} };
}
function dayFromCounters(date, c, uv) {
  const g = (k) => c[k] || {};
  const d = emptyDay(date);
  d.pages = g('pv'); d.convByPage = g('conv'); d.referrers = g('ref'); d.languages = g('lang'); d.ctaClicks = g('cta');
  d.abViews = g('ab_view'); d.abCta = g('ab_cta'); d.crawlers = g('crawl'); d.cats = g('cat'); d.catConv = g('catconv'); d.searches = g('search');
  d.uniqueVisitors = uv || 0;
  for (const k in d.pages) d.pageViews += d.pages[k];
  for (const k in d.convByPage) d.conversions += d.convByPage[k];
  return d;
}
function parseHash(result) {
  const hash = {}; const arr = (result && result.result) || [];
  for (let j = 0; j < arr.length; j += 2) hash[arr[j]] = parseInt(arr[j + 1]) || 0;
  return hash;
}
function dayFromRedis(results, offset, date) {
  const r = (k) => results[offset + FIELDS.indexOf(k)];
  const c = {}; for (const k of FIELDS) if (k !== 'uv') c[k] = parseHash(r(k));
  return dayFromCounters(date, c, (r('uv') && r('uv').result) || 0);
}
function quotaError(results) {
  if (!Array.isArray(results)) return (results && results.error) || 'KV error';
  for (const x of results) if (x && x.error && /max requests limit/i.test(x.error)) return x.error;
  return null;
}

function aggregate(dates, daily, totals, extra) {
  const acc = { topPages: {}, topReferrers: {}, topLanguages: {}, topCTAs: {}, abViews: {}, abCta: {}, topCats: {}, topCatConv: {}, topSearches: {}, crawlTotals: {} };
  let sumUV = 0, sumPV = 0, sumConv = 0;
  const add = (a, o) => { for (const k in o) a[k] = (a[k] || 0) + o[k]; };
  for (const day of daily) {
    sumPV += day.pageViews; sumUV += day.uniqueVisitors; sumConv += day.conversions;
    add(acc.topPages, day.pages); add(acc.topReferrers, day.referrers); add(acc.topLanguages, day.languages); add(acc.topCTAs, day.ctaClicks);
    add(acc.abViews, day.abViews); add(acc.abCta, day.abCta); add(acc.topCats, day.cats); add(acc.topCatConv, day.catConv); add(acc.topSearches, day.searches); add(acc.crawlTotals, day.crawlers);
  }
  const abSummary = {};
  const langOf = (p) => (p.includes('-en') ? 'en' : p.includes('-es') ? 'es' : p.includes('-pt') ? 'pt' : 'en');
  const bump = (map, field) => { for (const [key, count] of Object.entries(map)) { const [page, variant] = key.split('|'); const lang = langOf(page); if (!abSummary[lang]) abSummary[lang] = { a: { views: 0, cta: 0 }, b: { views: 0, cta: 0 } }; if (variant === 'a' || variant === 'b') abSummary[lang][variant][field] += count; } };
  bump(acc.abViews, 'views'); bump(acc.abCta, 'cta');
  const sorted = (o) => Object.entries(o).sort((a, b) => b[1] - a[1]);
  return Object.assign({
    period: { days: dates.length, from: dates[0], to: dates[dates.length - 1] },
    summary: { pageViews: sumPV, uniqueVisitors: sumUV, conversions: sumConv, conversionRate: sumUV > 0 ? ((sumConv / sumUV) * 100).toFixed(2) : '0.00' },
    daily,
    topPages: sorted(acc.topPages), topReferrers: sorted(acc.topReferrers), topLanguages: sorted(acc.topLanguages), topCTAs: sorted(acc.topCTAs),
    abSummary,
    topCategories: sorted(acc.topCats), topCategoryConv: sorted(acc.topCatConv), topSearches: sorted(acc.topSearches).slice(0, 100),
    crawlTotals: acc.crawlTotals,
    allTimeTotals: totals,
  }, extra || {});
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

  const days = Math.min(365, Math.max(1, parseInt(req.query.days) || 30));
  const dates = [];
  for (let i = days - 1; i >= 0; i--) { const d = new Date(); d.setDate(d.getDate() - i); dates.push(d.toISOString().slice(0, 10)); }
  const today = new Date().toISOString().slice(0, 10);

  const sb = supabase();
  if (sb) {
    try {
      const data = await sb.rpc('web_stats', { p_from: dates[0], p_to: dates[dates.length - 1] });
      const byDate = {};
      for (const d of (data && data.days) || []) byDate[d.date] = dayFromCounters(d.date, d.counters || {}, d.uv);
      const daily = dates.map((d) => byDate[d] || emptyDay(d));
      const t = (data && data.totals) || {};
      res.setHeader('Cache-Control', 's-maxage=120, stale-while-revalidate=300');
      return res.status(200).json(aggregate(dates, daily, { pageViews: parseInt(t.pv) || 0, conversions: parseInt(t.conv) || 0 }, { source: 'supabase' }));
    } catch (err) {
      console.error('Stats (supabase) error:', err && err.message);
      return res.status(503).json({ error: 'db', message: (err && err.message) || 'Supabase error' });
    }
  }

  const kv = upstash();
  if (!kv) return res.status(500).json({ error: 'store not configured' });
  try {
    const past = dates.filter((d) => d < today);
    const cached = {};
    if (past.length) {
      const r = await kv.pipeline(past.map((d) => ['GET', `analytics:day:${d}`]));
      const qe = quotaError(r); if (qe) return res.status(503).json({ error: 'kv_quota', message: qe });
      past.forEach((d, i) => { const v = r[i] && r[i].result; if (v) { try { cached[d] = JSON.parse(v); } catch (e) { /* recalcula */ } } });
    }
    const need = dates.filter((d) => !cached[d]);
    const pipeline = [];
    for (const date of need) for (const f of FIELDS) pipeline.push(f === 'uv' ? ['PFCOUNT', `analytics:uv:${date}`] : ['HGETALL', `analytics:${f}:${date}`]);
    pipeline.push(['GET', 'analytics:total:pv'], ['GET', 'analytics:total:conv']);
    const results = await kv.pipeline(pipeline);
    const qe = quotaError(results); if (qe) return res.status(503).json({ error: 'kv_quota', message: qe });
    const fresh = {};
    need.forEach((date, i) => { fresh[date] = dayFromRedis(results, i * FIELDS.length, date); });
    const totals = { pageViews: parseInt((results[need.length * FIELDS.length] || {}).result) || 0, conversions: parseInt((results[need.length * FIELDS.length + 1] || {}).result) || 0 };
    const toCache = need.filter((d) => d < today);
    if (toCache.length) { try { await kv.pipeline(toCache.map((d) => ['SET', `analytics:day:${d}`, JSON.stringify(fresh[d]), 'EX', DAY_CACHE_TTL])); } catch (e) { /* best effort */ } }
    const daily = dates.map((d) => cached[d] || fresh[d]);
    res.setHeader('Cache-Control', 's-maxage=120, stale-while-revalidate=300');
    res.status(200).json(aggregate(dates, daily, totals, { source: 'upstash', cache: { cachedDays: Object.keys(cached).length, rawDays: need.length } }));
  } catch (err) {
    console.error('Stats error:', err);
    res.status(500).json({ error: 'Failed to fetch analytics' });
  }
};

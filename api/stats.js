module.exports = async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  // Password check
  const password = req.query.password || req.headers['x-analytics-password'];
  const ANALYTICS_PASSWORD = process.env.ANALYTICS_PASSWORD;

  if (!ANALYTICS_PASSWORD || password !== ANALYTICS_PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const KV_URL = process.env.KV_REST_API_URL;
  const KV_TOKEN = process.env.KV_REST_API_TOKEN;

  if (!KV_URL || !KV_TOKEN) {
    return res.status(500).json({ error: 'KV not configured' });
  }

  try {
    const days = parseInt(req.query.days) || 30;

    // Generate date range
    const dates = [];
    for (let i = days - 1; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      dates.push(d.toISOString().slice(0, 10));
    }

    // Build pipeline to fetch all data for each date
    const pipeline = [];
    for (const date of dates) {
      pipeline.push(['HGETALL', `analytics:pv:${date}`]);
      pipeline.push(['PFCOUNT', `analytics:uv:${date}`]);
      pipeline.push(['HGETALL', `analytics:conv:${date}`]);
      pipeline.push(['HGETALL', `analytics:ref:${date}`]);
      pipeline.push(['HGETALL', `analytics:lang:${date}`]);
      pipeline.push(['HGETALL', `analytics:cta:${date}`]);
    }
    // Add totals
    pipeline.push(['GET', 'analytics:total:pv']);
    pipeline.push(['GET', 'analytics:total:conv']);

    const response = await fetch(`${KV_URL}/pipeline`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${KV_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(pipeline),
    });

    const results = await response.json();

    // Parse results into daily data
    const fieldsPerDay = 6;
    const daily = dates.map((date, i) => {
      const pvResult = results[i * fieldsPerDay];
      const uvResult = results[i * fieldsPerDay + 1];
      const convResult = results[i * fieldsPerDay + 2];
      const refResult = results[i * fieldsPerDay + 3];
      const langResult = results[i * fieldsPerDay + 4];
      const ctaResult = results[i * fieldsPerDay + 5];

      // Parse hash results (HGETALL returns flat array [key, val, key, val, ...])
      function parseHash(result) {
        const hash = {};
        const arr = (result && result.result) || [];
        for (let j = 0; j < arr.length; j += 2) {
          hash[arr[j]] = parseInt(arr[j + 1]) || 0;
        }
        return hash;
      }

      const pages = parseHash(pvResult);
      const conversions = parseHash(convResult);
      const referrers = parseHash(refResult);
      const languages = parseHash(langResult);
      const ctaClicks = parseHash(ctaResult);

      let totalPV = 0;
      for (const k in pages) totalPV += pages[k];

      let totalConv = 0;
      for (const k in conversions) totalConv += conversions[k];

      return {
        date,
        pageViews: totalPV,
        uniqueVisitors: (uvResult && uvResult.result) || 0,
        conversions: totalConv,
        pages,
        referrers,
        languages,
        ctaClicks,
      };
    });

    // Aggregate totals
    const totalPV = parseInt((results[dates.length * fieldsPerDay] || {}).result) || 0;
    const totalConv = parseInt((results[dates.length * fieldsPerDay + 1] || {}).result) || 0;

    // Aggregate top pages, referrers, languages, CTA clicks across all days
    const topPages = {};
    const topReferrers = {};
    const topLanguages = {};
    const topCTAs = {};
    let sumUV = 0;
    let sumPV = 0;
    let sumConv = 0;

    for (const day of daily) {
      sumPV += day.pageViews;
      sumUV += day.uniqueVisitors;
      sumConv += day.conversions;
      for (const p in day.pages) topPages[p] = (topPages[p] || 0) + day.pages[p];
      for (const r in day.referrers) topReferrers[r] = (topReferrers[r] || 0) + day.referrers[r];
      for (const l in day.languages) topLanguages[l] = (topLanguages[l] || 0) + day.languages[l];
      for (const c in day.ctaClicks) topCTAs[c] = (topCTAs[c] || 0) + day.ctaClicks[c];
    }

    res.status(200).json({
      period: { days, from: dates[0], to: dates[dates.length - 1] },
      summary: {
        pageViews: sumPV,
        uniqueVisitors: sumUV,
        conversions: sumConv,
        conversionRate: sumUV > 0 ? ((sumConv / sumUV) * 100).toFixed(2) : '0.00',
      },
      daily,
      topPages: Object.entries(topPages).sort((a, b) => b[1] - a[1]),
      topReferrers: Object.entries(topReferrers).sort((a, b) => b[1] - a[1]),
      topLanguages: Object.entries(topLanguages).sort((a, b) => b[1] - a[1]),
      topCTAs: Object.entries(topCTAs).sort((a, b) => b[1] - a[1]),
      allTimeTotals: { pageViews: totalPV, conversions: totalConv },
    });
  } catch (err) {
    console.error('Stats error:', err);
    res.status(500).json({ error: 'Failed to fetch analytics' });
  }
};

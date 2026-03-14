const crypto = require('crypto');

module.exports = async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const KV_URL = process.env.KV_REST_API_URL;
  const KV_TOKEN = process.env.KV_REST_API_TOKEN;

  if (!KV_URL || !KV_TOKEN) {
    return res.status(200).json({ ok: true, note: 'KV not configured' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') body = JSON.parse(body);

    const page = body.page || '/';
    const referrer = body.referrer || '';
    const event = body.event || 'pageview';
    const lang = body.lang || 'en';

    const now = new Date();
    const date = now.toISOString().slice(0, 10);

    // Create visitor fingerprint from IP + User-Agent + date
    const ip = (req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || '0.0.0.0').split(',')[0].trim();
    const ua = req.headers['user-agent'] || '';
    const visitorHash = crypto.createHash('sha256').update(ip + ua + date).digest('hex').slice(0, 16);

    // Build Redis pipeline
    const pipeline = [
      ['HINCRBY', `analytics:pv:${date}`, page, 1],
      ['PFADD', `analytics:uv:${date}`, visitorHash],
      ['INCR', 'analytics:total:pv'],
      ['HINCRBY', `analytics:lang:${date}`, lang, 1],
    ];

    // Track conversions (CTA clicks)
    if (event === 'conversion') {
      const ctaLabel = body.cta || 'unknown';
      pipeline.push(['HINCRBY', `analytics:conv:${date}`, page, 1]);
      pipeline.push(['INCR', 'analytics:total:conv']);
      // Track individual CTA clicks: "page|cta_label"
      pipeline.push(['HINCRBY', `analytics:cta:${date}`, ctaLabel, 1]);
    }

    // Track referrers
    if (referrer) {
      try {
        const refDomain = new URL(referrer).hostname;
        if (refDomain) {
          pipeline.push(['HINCRBY', `analytics:ref:${date}`, refDomain, 1]);
        }
      } catch (e) { /* ignore invalid referrer URLs */ }
    }

    await fetch(`${KV_URL}/pipeline`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${KV_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(pipeline),
    });

    res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Track error:', err);
    res.status(200).json({ ok: true });
  }
};

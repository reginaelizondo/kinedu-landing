// api/meta-analytics.js
// Vercel serverless function — proxies Meta Graph API for Learn campaign metrics

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const token = process.env.META_ACCESS_TOKEN;
  if (!token) {
    return res.status(500).json({ error: 'META_ACCESS_TOKEN not configured' });
  }

  const { date_preset = 'last_7d' } = req.query;

  const CAMPAIGNS = {
    en: { id: '120241984102940701', name: 'Learn EN (US)' },
    es: { id: '120242377179290701', name: 'Learn ES (MX)' },
  };

  const FIELDS = 'impressions,clicks,spend,ctr,cpc,actions,cost_per_action_type,reach,frequency';

  async function fetchInsights(campaignId) {
    const url = `https://graph.facebook.com/v19.0/${campaignId}/insights?fields=${FIELDS}&date_preset=${date_preset}&access_token=${token}`;
    const r = await fetch(url);
    const json = await r.json();
    if (json.error) throw new Error(json.error.message);
    return json.data && json.data.length > 0 ? json.data[0] : null;
  }

  async function fetchAdsets(campaignId) {
    const url = `https://graph.facebook.com/v19.0/${campaignId}/adsets?fields=id,name,status,effective_status&access_token=${token}`;
    const r = await fetch(url);
    const json = await r.json();
    return json.data || [];
  }

  async function fetchAdsetInsights(adsetId) {
    const url = `https://graph.facebook.com/v19.0/${adsetId}/insights?fields=${FIELDS}&date_preset=${date_preset}&access_token=${token}`;
    const r = await fetch(url);
    const json = await r.json();
    return json.data && json.data.length > 0 ? json.data[0] : null;
  }

  try {
    const results = {};

    for (const [lang, campaign] of Object.entries(CAMPAIGNS)) {
      const [insights, adsets] = await Promise.all([
        fetchInsights(campaign.id),
        fetchAdsets(campaign.id),
      ]);

      // Get top-level action counts
      const actions = insights?.actions || [];
      const offsite_conversions = actions.find(a => a.action_type === 'offsite_conversion.fb_pixel_custom')?.value || 0;
      const link_clicks = actions.find(a => a.action_type === 'link_click')?.value || 0;

      results[lang] = {
        name: campaign.name,
        campaign_id: campaign.id,
        date_preset,
        impressions: parseInt(insights?.impressions || 0),
        reach: parseInt(insights?.reach || 0),
        clicks: parseInt(insights?.clicks || 0),
        spend: parseFloat(insights?.spend || 0),
        ctr: parseFloat(insights?.ctr || 0),
        cpc: parseFloat(insights?.cpc || 0),
        link_clicks: parseInt(link_clicks),
        conversions: parseInt(offsite_conversions),
        adsets: adsets.length,
        has_data: !!insights,
      };
    }

    return res.status(200).json({
      ok: true,
      fetched_at: new Date().toISOString(),
      date_preset,
      campaigns: results,
    });

  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}

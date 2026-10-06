#!/usr/bin/env python3
"""Recolector semanal del agente de la landing (kinedu.com).

Junta en un solo JSON lo que el analista de los lunes necesita:
  - Search Console (API, cuenta de servicio): últimos 28 días vs los 28 anteriores,
    por fecha, página y consulta (clics, impresiones, CTR, posición).
  - Clarity (Data Export API): últimos 3 días, totales, por URL y por dispositivo.
    Se guarda cada corrida en history/ para acumular histórico (la API no da más de 3 días).
  - /api/stats de kinedu.com: visitas, conversiones, CTAs y A/B (últimos 14 días,
    partidos en semana actual vs anterior).

Secretos: ~/.config/kinedu-agent/.env (CLARITY_TOKEN, ANALYTICS_PASSWORD, GSC_KEY_FILE,
GSC_PROPERTY). Nunca se imprimen ni se escriben en la salida.

Uso:  ~/.config/kinedu-agent/venv/bin/python scripts/agent/weekly_pull.py [--clarity-only]
Salida: ~/.config/kinedu-agent/history/weekly-YYYY-MM-DD.json (o clarity-YYYY-MM-DD.json)
        y la ruta impresa al final.
"""
import os, sys, json, datetime, urllib.parse
import requests

HOME = os.path.expanduser("~")
CFG = os.path.join(HOME, ".config", "kinedu-agent")
HIST = os.path.join(CFG, "history")
os.makedirs(HIST, exist_ok=True)
TODAY = datetime.date.today()
CLARITY_ONLY = "--clarity-only" in sys.argv

env = {}
for line in open(os.path.join(CFG, ".env")):
    if "=" in line and not line.startswith("#"):
        k, v = line.strip().split("=", 1); env[k] = v.strip()
def secret(k):
    v = env.get(k, "")
    return "" if (not v or v.startswith("pega-aqui")) else v

out = {"generated": TODAY.isoformat(), "errors": []}

# ---------------- Clarity ----------------
def clarity():
    tok = secret("CLARITY_TOKEN")
    if not tok:
        out["errors"].append("clarity: sin token"); return
    base = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
    h = {"Authorization": "Bearer " + tok}
    res = {"days": 3}
    for name, params in (("totals", {"numOfDays": 3}), ("byUrl", {"numOfDays": 3, "dimension1": "URL"}), ("byDevice", {"numOfDays": 3, "dimension1": "Device"})):
        r = requests.get(base, headers=h, params=params, timeout=60)
        if r.status_code != 200:
            out["errors"].append(f"clarity {name}: http {r.status_code}"); continue
        res[name] = r.json()
    out["clarity"] = res
    with open(os.path.join(HIST, f"clarity-{TODAY.isoformat()}.json"), "w") as f:
        json.dump(res, f)

# ---------------- Search Console ----------------
def gsc():
    key = env.get("GSC_KEY_FILE", ""); prop = env.get("GSC_PROPERTY", "https://www.kinedu.com/")
    if not key or not os.path.exists(key):
        out["errors"].append("gsc: sin archivo de llave"); return
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
    except ImportError:
        out["errors"].append("gsc: falta google-auth en el venv"); return
    creds = service_account.Credentials.from_service_account_file(key, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    creds.refresh(Request())
    url = "https://www.googleapis.com/webmasters/v3/sites/" + urllib.parse.quote(prop, safe="") + "/searchAnalytics/query"
    H = {"Authorization": "Bearer " + creds.token}
    end = TODAY - datetime.timedelta(days=3)          # GSC tarda ~3 días en cerrar datos
    start = end - datetime.timedelta(days=27)
    pend = start - datetime.timedelta(days=1); pstart = pend - datetime.timedelta(days=27)
    def q(s, e, dims, limit=1000, filters=None):
        body = {"startDate": str(s), "endDate": str(e), "dimensions": dims, "rowLimit": limit}
        if filters: body["dimensionFilterGroups"] = [{"filters": filters}]
        r = requests.post(url, headers=H, json=body, timeout=120)
        if r.status_code != 200:
            out["errors"].append(f"gsc {dims}: http {r.status_code}"); return []
        return r.json().get("rows", [])
    def tot(rows):
        c = sum(x["clicks"] for x in rows); i = sum(x["impressions"] for x in rows)
        pos = (sum(x["position"] * x["impressions"] for x in rows) / i) if i else 0
        return {"clicks": c, "impressions": i, "ctr": (c / i * 100) if i else 0, "position": pos}
    cur_d = q(start, end, ["date"]); prev_d = q(pstart, pend, ["date"])
    cur_p = q(start, end, ["page"], 500); prev_p = q(pstart, pend, ["page"], 500)
    cur_q = q(start, end, ["query"], 500); prev_q = q(pstart, pend, ["query"], 500)
    def keyed(rows): return {x["keys"][0]: x for x in rows}
    pp, pq = keyed(prev_p), keyed(prev_q)
    def merge(cur, prev, n=40):
        items = []
        for x in cur:
            k = x["keys"][0]; p = prev.get(k)
            items.append({"key": k, "clicks": x["clicks"], "impressions": x["impressions"], "position": round(x["position"], 1),
                          "prev_clicks": p["clicks"] if p else 0, "prev_position": round(p["position"], 1) if p else None,
                          "delta_clicks": x["clicks"] - (p["clicks"] if p else 0)})
        top = sorted(items, key=lambda z: -z["clicks"])[:n]
        up = sorted(items, key=lambda z: -z["delta_clicks"])[:15]
        down = sorted(items, key=lambda z: z["delta_clicks"])[:15]
        new = [z for z in items if z["prev_clicks"] == 0 and z["clicks"] >= 3][:15]
        return {"top": top, "up": up, "down": down, "new": new}
    # ¿cuánto del tráfico es blog vs resto?
    def split(rows):
        b = sum(x["clicks"] for x in rows if "/blog/" in x["keys"][0]); t = sum(x["clicks"] for x in rows)
        return {"blog_clicks": b, "other_clicks": t - b}
    out["gsc"] = {
        "window": {"current": [str(start), str(end)], "previous": [str(pstart), str(pend)]},
        "current": tot(cur_d), "previous": tot(prev_d),
        "daily": [{"date": x["keys"][0], "clicks": x["clicks"], "impressions": x["impressions"], "position": round(x["position"], 1)} for x in cur_d],
        "pages": merge(cur_p, pp), "queries": merge(cur_q, pq),
        "split": {"current": split(cur_p), "previous": split(prev_p)},
    }

# ---------------- /api/stats ----------------
def site_stats():
    pw = secret("ANALYTICS_PASSWORD")
    if not pw:
        out["errors"].append("stats: sin ANALYTICS_PASSWORD en .env"); return
    r = requests.get("https://www.kinedu.com/api/stats", params={"days": 14, "password": pw}, timeout=120)
    if r.status_code != 200:
        out["errors"].append(f"stats: http {r.status_code}"); return
    d = r.json()
    daily = d.get("daily", [])
    def agg(days):
        pv = sum(x.get("pageViews", 0) for x in days); uv = sum(x.get("uniqueVisitors", 0) for x in days); cv = sum(x.get("conversions", 0) for x in days)
        return {"pageViews": pv, "uniqueVisitors": uv, "conversions": cv, "cvr": (cv / uv * 100) if uv else 0}
    out["site"] = {
        "thisWeek": agg(daily[-7:]), "prevWeek": agg(daily[:-7][-7:]),
        "topPages": d.get("topPages", [])[:25], "topCTAs": d.get("topCTAs", [])[:25], "topReferrers": d.get("topReferrers", [])[:15],
        "abSummary": d.get("abSummary", {}), "source": (d.get("meta") or {}).get("source"),
    }

clarity()
if not CLARITY_ONLY:
    gsc(); site_stats()
name = f"clarity-{TODAY.isoformat()}.json" if CLARITY_ONLY else f"weekly-{TODAY.isoformat()}.json"
path = os.path.join(HIST, name)
if not CLARITY_ONLY:
    with open(path, "w") as f: json.dump(out, f, indent=1, ensure_ascii=False)
print("errores:", out["errors"] or "ninguno")
print("salida:", path)

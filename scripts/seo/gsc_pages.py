#!/usr/bin/env python3
"""Search Console por página: clics, impresiones, posición, dispositivo y las consultas
principales de cada URL en los últimos N días (por defecto 90, cerrando 3 días antes de hoy).

Uso: ~/.config/kinedu-agent/venv/bin/python scripts/seo/gsc_pages.py [--days 90] /blog/slug [/es/blog/otro ...]
Lee GSC_KEY_FILE y GSC_PROPERTY de ~/.config/kinedu-agent/.env (misma llave que weekly_pull.py).
"""
import os, sys, json, datetime, urllib.parse
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

CFG = os.path.expanduser("~/.config/kinedu-agent")
env = {}
for line in open(os.path.join(CFG, ".env")):
    if "=" in line and not line.startswith("#"):
        k, v = line.strip().split("=", 1); env[k] = v.strip()

args = sys.argv[1:]
days = 90
if "--days" in args:
    i = args.index("--days"); days = int(args[i + 1]); del args[i:i + 2]
paths = args
if not paths:
    print(__doc__); sys.exit(1)

prop = env.get("GSC_PROPERTY", "https://www.kinedu.com/")
creds = service_account.Credentials.from_service_account_file(env["GSC_KEY_FILE"], scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
creds.refresh(Request())
url = "https://www.googleapis.com/webmasters/v3/sites/" + urllib.parse.quote(prop, safe="") + "/searchAnalytics/query"
H = {"Authorization": "Bearer " + creds.token}
end = datetime.date.today() - datetime.timedelta(days=3)
start = end - datetime.timedelta(days=days - 1)

def q(dims, page, limit=15):
    body = {"startDate": str(start), "endDate": str(end), "dimensions": dims, "rowLimit": limit,
            "dimensionFilterGroups": [{"filters": [{"dimension": "page", "operator": "equals", "expression": page}]}]}
    r = requests.post(url, headers=H, json=body, timeout=120)
    r.raise_for_status()
    return r.json().get("rows", [])

print(f"Search Console {start} a {end} ({days} días)")
for p in paths:
    full = prop.rstrip("/") + p
    tot = q(["page"], full, 1)
    t = tot[0] if tot else {"clicks": 0, "impressions": 0, "position": 0, "ctr": 0}
    print(f"\n== {p}\n   clics {t['clicks']} · impresiones {t['impressions']} · CTR {t['ctr']*100:.2f}% · posición {t['position']:.1f}")
    dev = q(["device"], full, 5)
    print("   dispositivo: " + ", ".join(f"{d['keys'][0].lower()} {d['clicks']}/{d['impressions']}" for d in dev))
    for x in q(["query"], full, 15):
        print(f"   {x['keys'][0]} | {x['clicks']} clics | {x['impressions']} impr | pos {x['position']:.1f}")

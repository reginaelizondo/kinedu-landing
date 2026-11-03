#!/usr/bin/env python3
"""Estado de los sitemaps en Search Console por API (sin Gmail). Imprime errores/avisos y sale 1 si hay errores.
Uso: ~/.config/kinedu-agent/venv/bin/python scripts/agent/gsc_sitemaps.py"""
import os, sys, urllib.parse, requests
env = {}
for l in open(os.path.expanduser("~/.config/kinedu-agent/.env")):
    if "=" in l and not l.startswith("#"):
        k, v = l.strip().split("=", 1); env[k] = v.strip().strip('"').strip("'")
from google.oauth2 import service_account
from google.auth.transport.requests import Request
creds = service_account.Credentials.from_service_account_file(env["GSC_KEY_FILE"], scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
creds.refresh(Request())
prop = env.get("GSC_PROPERTY", "https://www.kinedu.com/")
r = requests.get("https://www.googleapis.com/webmasters/v3/sites/" + urllib.parse.quote(prop, safe="") + "/sitemaps",
                 headers={"Authorization": "Bearer " + creds.token}, timeout=60)
if r.status_code != 200:
    print(f"ERROR http {r.status_code}: {r.text[:200]}"); sys.exit(2)
bad = 0
for s in r.json().get("sitemaps", []):
    e, w = int(s.get("errors", 0)), int(s.get("warnings", 0)); bad += e
    sub = sum(int(c.get("submitted", 0)) for c in s.get("contents", [])); idx = sum(int(c.get("indexed", 0)) for c in s.get("contents", []))
    print(f"{s.get('path')}: errores {e} · avisos {w} · enviadas {sub} · indexadas {idx} · descargado {str(s.get('lastDownloaded',''))[:10]} · pendiente {s.get('isPending')}")
print("RESULTADO:", "HAY ERRORES" if bad else "sin errores en sitemaps")
sys.exit(1 if bad else 0)

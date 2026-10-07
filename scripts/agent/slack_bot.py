#!/usr/bin/env python3
"""Marina (Claude): el bot de Slack del equipo de la landing.

Publica y lee en #landing-agente con el token del bot (SLACK_BOT_TOKEN en
~/.config/kinedu-agent/.env), para que los mensajes salgan firmados por la agente
y no por Regina. Nunca imprime el token.

Uso:
  slack_bot.py post  "texto"                  → publica un mensaje nuevo; imprime el ts
  slack_bot.py reply <ts> "texto"             → responde en el hilo de ese mensaje
  slack_bot.py read  [N]                      → últimos N mensajes del canal (JSON)
  slack_bot.py thread <ts>                    → todas las respuestas de ese hilo (JSON)
  slack_bot.py find  "prefijo"                → el mensaje más reciente del canal que empiece
                                                con ese texto (ignora emoji y formato), con su hilo
El texto acepta formato de Slack (mrkdwn): *negritas*, _cursivas_, `código`, listas con •.
Canal por defecto: C0C76H0F5F0 (#landing-agente); se puede cambiar con SLACK_CHANNEL en .env.
"""
import os, sys, json, re, urllib.request, urllib.parse

CFG = os.path.expanduser("~/.config/kinedu-agent/.env")
env = {}
for line in open(CFG):
    if "=" in line and not line.startswith("#"):
        k, v = line.strip().split("=", 1); env[k] = v.strip()
TOKEN = env.get("SLACK_BOT_TOKEN", "")
CHANNEL = env.get("SLACK_CHANNEL", "C0C76H0F5F0")
if not TOKEN.startswith("xoxb-"):
    print(json.dumps({"ok": False, "error": "sin SLACK_BOT_TOKEN en ~/.config/kinedu-agent/.env"})); sys.exit(1)

def api(method, params=None, post=False):
    url = "https://slack.com/api/" + method
    headers = {"Authorization": "Bearer " + TOKEN}
    if post:
        data = json.dumps(params or {}).encode()
        headers["Content-Type"] = "application/json; charset=utf-8"
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    else:
        req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params or {}), headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def strip(t):
    return re.sub(r"[^\w]+", " ", (t or "").lower()).strip()

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "post":
        r = api("chat.postMessage", {"channel": CHANNEL, "text": sys.argv[2], "unfurl_links": False}, post=True)
        print(json.dumps({"ok": r.get("ok"), "ts": r.get("ts"), "error": r.get("error")}))
    elif cmd == "reply":
        r = api("chat.postMessage", {"channel": CHANNEL, "thread_ts": sys.argv[2], "text": sys.argv[3], "unfurl_links": False}, post=True)
        print(json.dumps({"ok": r.get("ok"), "ts": r.get("ts"), "error": r.get("error")}))
    elif cmd == "read":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        r = api("conversations.history", {"channel": CHANNEL, "limit": n})
        msgs = [{"ts": m.get("ts"), "user": m.get("user"), "bot": m.get("bot_id"), "text": m.get("text", ""), "replies": m.get("reply_count", 0)} for m in r.get("messages", [])]
        print(json.dumps({"ok": r.get("ok"), "error": r.get("error"), "messages": msgs}, ensure_ascii=False, indent=1))
    elif cmd == "thread":
        r = api("conversations.replies", {"channel": CHANNEL, "ts": sys.argv[2], "limit": 200})
        msgs = [{"ts": m.get("ts"), "user": m.get("user"), "bot": m.get("bot_id"), "text": m.get("text", "")} for m in r.get("messages", [])]
        print(json.dumps({"ok": r.get("ok"), "error": r.get("error"), "messages": msgs}, ensure_ascii=False, indent=1))
    elif cmd == "find":
        want = strip(sys.argv[2])
        r = api("conversations.history", {"channel": CHANNEL, "limit": 100})
        for m in r.get("messages", []):
            if strip(m.get("text", "")).startswith(want):
                t = api("conversations.replies", {"channel": CHANNEL, "ts": m["ts"], "limit": 200})
                out = {"ok": True, "ts": m["ts"], "text": m.get("text", ""),
                       "replies": [{"ts": x.get("ts"), "user": x.get("user"), "bot": x.get("bot_id"), "text": x.get("text", "")} for x in t.get("messages", [])[1:]]}
                print(json.dumps(out, ensure_ascii=False, indent=1)); return
        print(json.dumps({"ok": False, "error": "no encontrado"}))
    else:
        print(__doc__); sys.exit(1)

main()

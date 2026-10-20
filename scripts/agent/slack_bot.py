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
  slack_bot.py propose <spec.json>            → publica propuestas con botones ✅ Acepto / ✖ No por ahora
                                                (Block Kit). spec: {"titulo","intro"?,"fecha"?,"items":[{"n","titulo",
                                                "detalle","impacto"?,"se_ve"?,"dueno"?,"calculo"?,"riesgo"?,"emoji"?,"id"?}]}
                                                El clic llega a kinedu.com/masterclasses/api/slack/interact y queda guardado.
  slack_bot.py approvals [dias]               → decisiones tomadas con los botones (JSON), vía
                                                /masterclasses/api/admin/approvals (llave ANALYTICS_PASSWORD)
El texto acepta formato de Slack (mrkdwn): *negritas*, _cursivas_, `código`, listas con •.
Canal por defecto: C0C76H0F5F0 (#landing-agente); se puede cambiar con SLACK_CHANNEL en .env.
"""
import os, sys, json, re, datetime, urllib.request, urllib.parse

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
    elif cmd == "propose":
        spec = json.load(open(sys.argv[2], encoding="utf-8"))
        fecha = spec.get("fecha") or datetime.date.today().isoformat()
        def pid(it): return it.get("id") or f"{fecha}-{it['n']}"
        blocks = [{"type": "header", "text": {"type": "plain_text", "text": str(spec.get("titulo", "Recomendaciones"))[:150], "emoji": True}}]
        if spec.get("intro"):
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": str(spec["intro"])[:2900]}})
        for it in spec["items"]:
            head = f"*{it['n']}. {it.get('emoji', '')} {it['titulo']}*".replace("  ", " ")
            if it.get("impacto"): head += f" · *{it['impacto']}*"
            if it.get("se_ve"): head += f" · se ve en {it['se_ve']}"
            if it.get("dueno"): head += f" · dueño: {it['dueno']}"
            body = str(it.get("detalle", ""))
            if it.get("calculo"): body += f"\n_Cómo se calculó:_ {it['calculo']}"
            if it.get("riesgo"): body += f"\n_Riesgo:_ {it['riesgo']}"
            val = json.dumps({"id": pid(it), "n": it["n"], "titulo": str(it["titulo"])[:80]}, ensure_ascii=False)
            blocks += [
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": (head + "\n" + body)[:2900]}},
                {"type": "actions", "block_id": f"acc-{pid(it)}"[:255], "elements": [
                    {"type": "button", "style": "primary", "action_id": "aprobar", "text": {"type": "plain_text", "text": "✅ Acepto", "emoji": True}, "value": val},
                    {"type": "button", "action_id": "rechazar", "text": {"type": "plain_text", "text": "✖ No por ahora", "emoji": True}, "value": val},
                ]},
            ]
        fallback = str(spec.get("titulo", "Recomendaciones")) + ": " + "; ".join(f"{i['n']}. {i['titulo']}" for i in spec["items"])
        r = api("chat.postMessage", {"channel": CHANNEL, "text": fallback, "blocks": blocks, "unfurl_links": False}, post=True)
        print(json.dumps({"ok": r.get("ok"), "ts": r.get("ts"), "error": r.get("error"), "ids": [pid(i) for i in spec["items"]]}, ensure_ascii=False))
    elif cmd == "approvals":
        days = sys.argv[2] if len(sys.argv) > 2 else "14"
        req = urllib.request.Request("https://www.kinedu.com/masterclasses/api/admin/approvals?days=" + urllib.parse.quote(days),
                                     headers={"x-metrics-key": env.get("ANALYTICS_PASSWORD", "")})
        with urllib.request.urlopen(req, timeout=30) as r:
            print(r.read().decode("utf-8"))
    else:
        print(__doc__); sys.exit(1)

main()

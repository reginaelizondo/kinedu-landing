#!/usr/bin/env python3
"""Bitácora de Marina: el registro único de todo lo que hace el agente de la landing.

Para qué: que cada cambio quede anotado con su porqué, cuándo se mide y, cuando se
mide, su resultado y el aprendizaje. Así Regina VE el avance (tablero) y Marina
APRENDE (lee aprendizajes.md antes de actuar y no repite errores).

Una sola fuente de verdad: 00-memoria/bitacora.jsonl (una línea JSON por entrada,
append-only). De ahí se generan el BITACORA.md legible y el tablero HTML. Las
rutinas NUNCA editan los .md a mano: solo llaman a este script.

Uso:
  bitacora.py add rol=Implementador tipo=cambio area=SEO estado=publicado \\
        commit=abc123 medir_en=2026-11-03 titulo="..." detalle="..."
  bitacora.py set <id> resultado="..." impacto=win aprendizaje="..."   # el Medidor lo cierra
  bitacora.py aprende "regla corta que aplica siempre"  [area=SEO]      # sube un aprendizaje
  bitacora.py report                 # resumen para Slack (formato de Regina) + regenera md/html
  bitacora.py sync                   # solo regenera BITACORA.md y el tablero HTML
  bitacora.py list [N]               # últimas N entradas (JSON)

Campos de una entrada:
  id fecha rol tipo area titulo detalle commit estado medir_en resultado impacto aprendizaje
  tipo   : cambio | medicion | alerta | decision | aprendizaje
  estado : publicado | preview | pendiente | revertido | na
  impacto: win | neutral | loss | pendiente
"""
import os, sys, json, datetime, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MEM = os.path.join(REPO, "agente-landing", "00-memoria")
JSONL = os.path.join(MEM, "bitacora.jsonl")
MD = os.path.join(MEM, "BITACORA.md")
APRE = os.path.join(MEM, "aprendizajes.md")
DASH_DIR = os.path.expanduser("~/Downloads/Marina-Avance")
DASH = os.path.join(DASH_DIR, "avance.html")
TODAY = datetime.date.today().isoformat()

AREAS = ("SEO", "Gift", "Masterclasses", "Landing", "A/B", "Contenido", "Infra", "Proceso")
FIELDS = ("id", "fecha", "rol", "tipo", "area", "titulo", "detalle", "commit",
          "estado", "medir_en", "resultado", "impacto", "aprendizaje")

def load():
    if not os.path.exists(JSONL):
        return []
    out = []
    for line in open(JSONL, encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out

def append(entry):
    with open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def rewrite(rows):
    with open(JSONL, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def parse_kv(args):
    d = {}
    for a in args:
        if "=" in a:
            k, v = a.split("=", 1)
            d[k.strip()] = v.strip()
    return d

def new_id(rows):
    n = sum(1 for r in rows if r.get("fecha") == TODAY) + 1
    return f"{TODAY}-{n:02d}"

def cmd_add(args):
    rows = load()
    kv = parse_kv(args)
    e = {k: "" for k in FIELDS}
    e["id"] = new_id(rows)
    e["fecha"] = kv.get("fecha", TODAY)
    e["rol"] = kv.get("rol", "Marina")
    e["tipo"] = kv.get("tipo", "cambio")
    e["area"] = kv.get("area", "Landing")
    e["titulo"] = kv.get("titulo", "")
    e["detalle"] = kv.get("detalle", "")
    e["commit"] = kv.get("commit", "")
    e["estado"] = kv.get("estado", "publicado")
    e["medir_en"] = kv.get("medir_en", "")
    e["resultado"] = kv.get("resultado", "")
    e["impacto"] = kv.get("impacto", "pendiente" if e["tipo"] == "cambio" else "")
    e["aprendizaje"] = kv.get("aprendizaje", "")
    if not e["titulo"]:
        print("falta titulo="); sys.exit(1)
    append(e)
    sync()
    print("anotado:", e["id"], "·", e["titulo"])

def cmd_set(args):
    if not args:
        print("uso: set <id> campo=valor ..."); sys.exit(1)
    rid = args[0]; kv = parse_kv(args[1:])
    rows = load(); hit = None
    for r in rows:
        if r.get("id") == rid:
            hit = r
            for k, v in kv.items():
                if k in FIELDS:
                    r[k] = v
            break
    if not hit:
        print("no existe id", rid); sys.exit(1)
    rewrite(rows); sync()
    print("actualizado:", rid)

def cmd_aprende(args):
    if not args:
        print('uso: aprende "texto" [area=SEO]'); sys.exit(1)
    kv = parse_kv(args)
    texto = " ".join(a for a in args if "=" not in a).strip()
    area = kv.get("area", "General")
    linea = f"- **[{area}]** {texto} _(anotado {TODAY})_\n"
    head = "# Aprendizajes de Marina\n\nReglas cortas que Marina debe leer ANTES de actuar. Se suben desde la bitácora cuando una medición deja una lección. No repetir lo que ya está aquí.\n\n"
    body = ""
    if os.path.exists(APRE):
        cur = open(APRE, encoding="utf-8").read()
        body = cur.split("\n", 0)[0] if False else cur[cur.find("\n\n", cur.find("# Aprendizajes")) + 2:] if "# Aprendizajes" in cur else cur
    with open(APRE, "w", encoding="utf-8") as f:
        f.write(head + linea + body)
    # también lo deja como entrada tipo aprendizaje
    cmd_add([f"rol={kv.get('rol','Marina')}", "tipo=aprendizaje", f"area={area}",
             f"titulo={texto[:80]}", "estado=na"])
    print("aprendizaje guardado")

def wk(fecha):
    try:
        d = datetime.date.fromisoformat(fecha)
    except Exception:
        return fecha
    monday = d - datetime.timedelta(days=d.weekday())
    return monday.isoformat()

# ---------------- render markdown ----------------
def sync():
    rows = load()
    rows_sorted = sorted(rows, key=lambda r: (r.get("fecha", ""), r.get("id", "")))
    # agrupar por semana (lunes)
    weeks = {}
    for r in rows_sorted:
        weeks.setdefault(wk(r.get("fecha", "")), []).append(r)
    ICON = {"cambio": "🔧", "medicion": "📊", "alerta": "⚠️", "decision": "🧭", "aprendizaje": "💡"}
    IMP = {"win": "✅ win", "neutral": "➖ neutral", "loss": "❌ loss", "pendiente": "⏳ por medir", "": ""}
    lines = ["# Bitácora de Marina\n",
             "Registro único de lo que hace el agente de la landing. Generado desde `bitacora.jsonl` (no editar a mano; usar `scripts/agent/bitacora.py`).\n",
             f"Última actualización: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}.\n"]
    for w in sorted(weeks, reverse=True):
        lines.append(f"\n## Semana del {w}\n")
        for r in weeks[w]:
            ic = ICON.get(r.get("tipo"), "•")
            head = f"- {ic} **{r.get('id')}** · {r.get('area')} · {r.get('titulo')}  _({r.get('rol')})_"
            lines.append(head)
            meta = []
            if r.get("estado") and r["estado"] != "na":
                meta.append(f"estado: {r['estado']}")
            if r.get("commit"):
                meta.append(f"commit {r['commit']}")
            if r.get("medir_en"):
                meta.append(f"medir: {r['medir_en']}")
            if r.get("impacto"):
                meta.append(IMP.get(r["impacto"], r["impacto"]))
            if meta:
                lines.append(f"  - _{' · '.join(meta)}_")
            if r.get("detalle"):
                lines.append(f"  - {r['detalle']}")
            if r.get("resultado"):
                lines.append(f"  - **Resultado:** {r['resultado']}")
            if r.get("aprendizaje"):
                lines.append(f"  - **Aprendizaje:** {r['aprendizaje']}")
    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    render_html(rows_sorted)

def count_aprendizajes():
    if not os.path.exists(APRE):
        return 0
    return sum(1 for ln in open(APRE, encoding="utf-8") if re.match(r"- \*\*\[.+?\]\*\* ", ln.strip()))

def stats(rows):
    cambios = [r for r in rows if r.get("tipo") == "cambio"]
    pub = [r for r in cambios if r.get("estado") == "publicado"]
    medidos = [r for r in cambios if r.get("impacto") in ("win", "neutral", "loss")]
    wins = [r for r in cambios if r.get("impacto") == "win"]
    loss = [r for r in cambios if r.get("impacto") == "loss"]
    neu = [r for r in cambios if r.get("impacto") == "neutral"]
    porm = [r for r in cambios if r.get("impacto") == "pendiente" and r.get("estado") == "publicado"]
    return dict(total=len(rows), cambios=len(cambios), pub=len(pub), medidos=len(medidos),
                wins=len(wins), loss=len(loss), neu=len(neu), porm=len(porm), apr=count_aprendizajes(),
                _porm=porm, _wins=wins, _loss=loss)

# ---------------- render HTML dashboard ----------------
def render_html(rows):
    os.makedirs(DASH_DIR, exist_ok=True)
    s = stats(rows)
    esc = lambda x: html.escape(str(x or ""))
    ICON = {"cambio": "🔧", "medicion": "📊", "alerta": "⚠️", "decision": "🧭", "aprendizaje": "💡"}
    IMPCL = {"win": "win", "neutral": "neu", "loss": "loss", "pendiente": "pend", "": ""}
    IMPTX = {"win": "win", "neutral": "neutral", "loss": "loss", "pendiente": "por medir", "": ""}
    # timeline filas (más reciente primero)
    tl = []
    for r in sorted(rows, key=lambda r: (r.get("fecha", ""), r.get("id", "")), reverse=True):
        imp = r.get("impacto", "")
        chip = f'<span class="chip {IMPCL.get(imp,"")}">{IMPTX.get(imp,"")}</span>' if imp else ""
        extra = ""
        if r.get("resultado"):
            extra += f'<div class="res"><b>Resultado:</b> {esc(r["resultado"])}</div>'
        if r.get("aprendizaje"):
            extra += f'<div class="apr"><b>Aprendizaje:</b> {esc(r["aprendizaje"])}</div>'
        meta = []
        if r.get("estado") and r["estado"] != "na": meta.append(esc(r["estado"]))
        if r.get("commit"): meta.append("commit " + esc(r["commit"]))
        if r.get("medir_en"): meta.append("medir " + esc(r["medir_en"]))
        tl.append(f"""<div class="row">
          <div class="when">{esc(r.get('fecha'))}<span class="rol">{esc(r.get('rol'))}</span></div>
          <div class="body">
            <div class="t">{ICON.get(r.get('tipo'),'•')} <span class="area">{esc(r.get('area'))}</span> {esc(r.get('titulo'))} {chip}</div>
            <div class="meta">{' · '.join(meta)}</div>
            <div class="det">{esc(r.get('detalle'))}</div>
            {extra}
          </div></div>""")
    # aprendizajes list
    apr_items = ""
    if os.path.exists(APRE):
        for ln in open(APRE, encoding="utf-8"):
            m = re.match(r"- \*\*\[(.+?)\]\*\* (.+?)(?: _\(anotado (.+?)\)_)?\s*$", ln.strip())
            if m:
                apr_items += f'<li><span class="area">{esc(m.group(1))}</span> {esc(m.group(2))}</li>'
    if not apr_items:
        apr_items = '<li class="muted">Aún no hay aprendizajes registrados.</li>'
    medidos_pct = round(s["medidos"] / s["pub"] * 100) if s["pub"] else 0
    win_pct = round(s["wins"] / s["medidos"] * 100) if s["medidos"] else 0
    doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Avance de Marina</title>
<style>
:root{{--bg:#FCFBF9;--card:#FFFFFF;--ink:#2B2E3A;--body:#5B6170;--muted:#9AA0AD;--border:#EFEDE6;
 --blue:#0086D8;--win:#3EB646;--loss:#EC4D4D;--neu:#9AA0AD;--pend:#F9BA48;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:'Proxima Nova',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;line-height:1.5;padding:28px 18px 60px}}
.wrap{{max-width:860px;margin:0 auto}}
h1{{font-size:26px;letter-spacing:-.02em}}
h1 .b{{color:var(--blue)}}
.sub{{color:var(--muted);font-size:13px;margin:4px 0 22px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-bottom:12px}}
.c{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px}}
.c .n{{font-size:28px;font-weight:800;letter-spacing:-.02em}}
.c .l{{font-size:12px;color:var(--body);font-weight:600;margin-top:2px}}
.c.win .n{{color:var(--win)}}.c.loss .n{{color:var(--loss)}}.c.blue .n{{color:var(--blue)}}.c.pend .n{{color:#D9931F}}
.bar{{height:10px;border-radius:999px;background:var(--border);overflow:hidden;margin-top:8px;display:flex}}
.bar i{{display:block;height:100%}}
.bar .w{{background:var(--win)}}.bar .nn{{background:var(--neu)}}.bar .ll{{background:var(--loss)}}
h2{{font-size:16px;margin:26px 0 10px}}
.apr{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 18px}}
.apr ul{{list-style:none}} .apr li{{padding:6px 0;border-bottom:1px solid var(--border);font-size:14px}}
.apr li:last-child{{border:0}}
.area{{display:inline-block;background:rgba(0,134,216,.1);color:var(--blue);font-size:11px;font-weight:700;padding:1px 7px;border-radius:6px;margin-right:6px;vertical-align:middle}}
.row{{display:flex;gap:14px;background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 16px;margin-bottom:10px}}
.when{{flex:0 0 92px;font-size:12px;color:var(--muted);font-weight:600}}
.when .rol{{display:block;color:var(--body);font-weight:700;margin-top:3px}}
.body{{flex:1;min-width:0}}
.t{{font-weight:700;font-size:15px}}
.meta{{font-size:12px;color:var(--muted);margin:3px 0}}
.det{{font-size:13.5px;color:var(--body);margin-top:4px}}
.res,.apr{{font-size:13px;margin-top:5px}} .body .res{{color:var(--ink)}} .body .apr{{color:#7a5b00;background:none;border:0;padding:0}}
.chip{{display:inline-block;font-size:11px;font-weight:800;padding:1px 8px;border-radius:999px;vertical-align:middle;color:#fff}}
.chip.win{{background:var(--win)}}.chip.loss{{background:var(--loss)}}.chip.neu{{background:var(--neu)}}.chip.pend{{background:var(--pend);color:#5a4500}}
.muted{{color:var(--muted)}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161A26;--card:#222838;--ink:#F5F6FA;--body:#C7CBD8;--muted:#8A90A0;--border:#333A4C}}}}
</style></head><body><div class="wrap">
<h1>Avance de <span class="b">Marina</span></h1>
<div class="sub">Bitácora del agente de la landing · generado {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
<div class="cards">
 <div class="c blue"><div class="n">{s['cambios']}</div><div class="l">cambios registrados</div></div>
 <div class="c"><div class="n">{s['pub']}</div><div class="l">publicados</div></div>
 <div class="c win"><div class="n">{s['wins']}</div><div class="l">wins medidos</div></div>
 <div class="c pend"><div class="n">{s['porm']}</div><div class="l">por medir</div></div>
 <div class="c"><div class="n">{s['apr']}</div><div class="l">aprendizajes</div></div>
</div>
<div class="c">
 <div class="l" style="font-weight:700;margin-bottom:2px">Resultado de lo ya medido ({s['medidos']} de {s['pub']} publicados · {medidos_pct}% medido)</div>
 <div class="bar"><i class="w" style="width:{ (s['wins']/max(s['medidos'],1))*100 }%"></i><i class="nn" style="width:{ (s['neu']/max(s['medidos'],1))*100 }%"></i><i class="ll" style="width:{ (s['loss']/max(s['medidos'],1))*100 }%"></i></div>
 <div class="l" style="margin-top:6px">✅ {s['wins']} win · ➖ {s['neu']} neutral · ❌ {s['loss']} loss</div>
</div>
<h2>💡 Aprendizajes (lo que Marina ya sabe)</h2>
<div class="apr"><ul>{apr_items}</ul></div>
<h2>🗓️ Línea de tiempo</h2>
{''.join(tl)}
</div></body></html>"""
    with open(DASH, "w", encoding="utf-8") as f:
        f.write(doc)

def cmd_report():
    rows = load(); sync(); s = stats(rows)
    porm = sorted(s["_porm"], key=lambda r: r.get("medir_en", "zzz"))
    print("*📔 Avance de Marina*")
    print(f"• *{s['cambios']}* cambios registrados · *{s['pub']}* publicados · *{s['apr']}* aprendizajes")
    print(f"• Medido: *{s['wins']}* win · {s['neu']} neutral · {s['loss']} loss · *{s['porm']}* por medir")
    if porm:
        print("• Próximas mediciones:")
        for r in porm[:5]:
            print(f"   - {r.get('medir_en') or '¿?'} · {r.get('area')} · {r.get('titulo')}")
    print(f"\nTablero: {DASH}")

def main():
    os.makedirs(MEM, exist_ok=True)
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    cmd = sys.argv[1]; rest = sys.argv[2:]
    if cmd == "add": cmd_add(rest)
    elif cmd == "set": cmd_set(rest)
    elif cmd == "aprende": cmd_aprende(rest)
    elif cmd == "report": cmd_report()
    elif cmd == "sync": sync(); print("regenerado:", MD, "y", DASH)
    elif cmd == "list":
        n = int(rest[0]) if rest else 15
        for r in load()[-n:]:
            print(json.dumps(r, ensure_ascii=False))
    else:
        print(__doc__)

main()

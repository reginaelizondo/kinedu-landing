#!/usr/bin/env python3
"""Genera las imágenes Open Graph (1200x630) de las páginas principales.

Uso: con el servidor local corriendo en http://localhost:8090 (preview
"landing-page"), `python3 scripts/og/build.py` escribe og-*.png en la raíz.
Requiere Playwright (venv del scratchpad o `pip install playwright`).
Las plantillas se escriben en _preview/ (ignorado por git) para que las
fuentes Proxima Nova carguen desde el mismo origen."""
import asyncio, html, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.environ.get("OG_BASE", "http://localhost:8090")

# (archivo, headline parte normal, headline parte azul, tagline)
ITEMS = {
  "og-image":            ("Know exactly what to do with your baby,", "every single day.", "Trusted by 11M+ families · Research based · Recommended by pediatricians"),
  "og-image-es":         ("Descubre exactamente qué hacer con tu bebé,", "cada día.", "+11M de familias · Basado en investigación · Recomendado por pediatras"),
  "og-image-pt":         ("Descubra exatamente o que fazer com o seu bebê,", "todos os dias.", "11M+ famílias · Baseado em pesquisa · Recomendado por pediatras"),
  "og-gift":             ("The gift that grows", "with their baby.", "A year of Kinedu: daily activity plans, live expert classes and more"),
  "og-gift-es":          ("El regalo que crece", "con su bebé.", "Un año de Kinedu: plan diario de actividades, clases en vivo con expertos y más"),
  "og-gift-pt":          ("O presente que cresce", "com o bebê.", "Um ano de Kinedu: plano diário de atividades, aulas ao vivo com especialistas e mais"),
  "og-masterclasses":    ("Expert courses for", "the real first years.", "Newborn first aid · Sleep · Feeding · Development · Certified experts"),
  "og-masterclasses-es": ("Cursos de expertos para", "los primeros años de verdad.", "Primeros auxilios · Sueño · Alimentación · Desarrollo · Expertos certificados"),
  "og-masterclasses-pt": ("Cursos de especialistas para", "os primeiros anos de verdade.", "Primeiros socorros · Sono · Alimentação · Desenvolvimento · Especialistas certificados"),
  "og-experts":          ("Real credentials.", "Real experience.", "Pediatricians · Sleep coaches · Lactation · Feeding · Psychologists"),
}

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Proxima Nova';src:url(/fonts/proxima-nova/proximanova-regular-webfont.woff2) format('woff2');font-weight:400}}
@font-face{{font-family:'Proxima Nova';src:url(/fonts/proxima-nova/proximanova-bold-webfont.woff2) format('woff2');font-weight:700}}
html,body{{margin:0}}
body{{width:1200px;height:630px;overflow:hidden;font-family:'Proxima Nova',Helvetica,Arial,sans-serif;background:linear-gradient(180deg,#EEF6FF 0%,#FBFAF8 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;position:relative}}
.logo{{position:absolute;top:72px;left:50%;transform:translateX(-50%);height:74px}}
h1{{margin:0;padding:0 90px;font-size:{fs}px;line-height:1.14;font-weight:700;color:#1E2A44;letter-spacing:-0.02em;text-wrap:balance}}
h1 span{{color:#0086D8;display:block}}
p{{margin:26px 0 0;padding:0 90px;font-size:27px;color:#5B6478;font-weight:400}}
</style></head><body>
<img class="logo" src="/logo kinedu.png" alt="">
<div style="margin-top:80px"><h1>{h1}<span>{h2}</span></h1><p>{tag}</p></div>
</body></html>"""

async def main(only=None):
    from playwright.async_api import async_playwright
    prev = os.path.join(ROOT, "_preview"); os.makedirs(prev, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        ctx = await b.new_context(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        pg = await ctx.new_page()
        for name, (h1, h2, tag) in ITEMS.items():
            if only and name not in only: continue
            fs = 60 if len(h1) + len(h2) <= 52 else 54
            open(os.path.join(prev, f"_og-{name}.html"), "w", encoding="utf-8").write(
                TPL.format(h1=html.escape(h1), h2=html.escape(h2), tag=html.escape(tag), fs=fs))
            await pg.goto(f"{BASE}/_preview/_og-{name}.html"); await pg.wait_for_timeout(400)
            await pg.evaluate("document.fonts.ready")
            out = os.path.join(ROOT, f"{name}.png")
            await pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
            print(name, os.path.getsize(out) // 1024, "KB")
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:]) or None))

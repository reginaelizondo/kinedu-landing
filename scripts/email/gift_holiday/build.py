#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la campaña de temporada "Regala Kinedu": heros PNG + HTML para CleverTap (EN/ES/PT).
   python3 scripts/email/gift_holiday/build.py            -> HTML con imagenes en kinedu.com (para CleverTap)
   python3 scripts/email/gift_holiday/build.py --local    -> ademas, copia de preview con imagenes locales
Reglas (ver memoria clevertap-email-rules): sin header/footer, una columna, sin depender de @media, boton debajo del
texto, un solo bloque Liquid (saludo) con rama sin nombre, & literal en links, #no_universal_links."""
import os, sys, urllib.parse, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gift_copy as C, hero as HERO
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
IMG_DIR = os.path.join(REPO, "email", "gift", "holiday")
IMG_URL = "https://www.kinedu.com/email/gift/holiday/"
OUT = os.path.expanduser("~/Downloads/gift-holiday-2026-clevertap")
FF = "'Proxima Nova','Plus Jakarta Sans','Avenir Next','Segoe UI',Helvetica,Arial,sans-serif"
INK, BODY, MUTED, BLUE, PINK, GREEN, YELLOW, CTA, BG = "#2B2E3A", "#5B6170", "#8A90A0", "#0086D8", "#DA4D7A", "#45C94E", "#F9BA48", "#E57339", "#FCFBF9"
DOTS = [BLUE, PINK, GREEN, YELLOW]

STYLE = """
:root{color-scheme:light dark;supported-color-schemes:light dark}
@media (prefers-color-scheme: dark){
  .bg{background:#1A1D2E!important}
  .card{background:#262A3C!important;border-color:#343949!important}
  .tint{background:#2B2A24!important;border-color:#4A4330!important}
  .ink{color:#F5F6FA!important}
  .body{color:#C7CBD8!important}
  .muted{color:#9AA0AD!important}
  .blue{color:#5AB8F0!important}
  .hair{border-color:#343949!important}
  .btn2{color:#F5F6FA!important;border-color:#5B6170!important}
}
[data-ogsc] .bg{background:#1A1D2E!important}
[data-ogsc] .card{background:#262A3C!important;border-color:#343949!important}
[data-ogsc] .tint{background:#2B2A24!important;border-color:#4A4330!important}
[data-ogsc] .ink{color:#F5F6FA!important}
[data-ogsc] .body{color:#C7CBD8!important}
[data-ogsc] .muted{color:#9AA0AD!important}
[data-ogsc] .blue{color:#5AB8F0!important}
[data-ogsc] .hair{border-color:#343949!important}
[data-ogsc] .btn2{color:#F5F6FA!important;border-color:#5B6170!important}
"""

def link(lang, eid):
    return C.GIFT_URL[lang] + "?utm_source=email&utm_medium=lifecycle&utm_campaign=" + C.CAMPAIGN + "&utm_content=" + eid + "#no_universal_links"

def wa_link(lang, text):
    url = C.GIFT_URL[lang] + "?utm_source=whatsapp&utm_medium=share&utm_campaign=" + C.CAMPAIGN
    return "https://wa.me/?text=" + urllib.parse.quote(text + " " + url, safe="")

def row(inner, pad="0 0 0 0", align=None, cls=None, extra=""):
    a = ' align="%s"' % align if align else ""
    c = ' class="%s"' % cls if cls else ""
    return '<tr><td%s%s style="padding:%s;%s">%s</td></tr>\n' % (a, c, pad, extra, inner)

def text_row(t, size=16, color=BODY, cls="body", pad="0 0 12px", weight=400, align=None, lh=1.65, extra=""):
    a = ' align="%s"' % align if align else ""
    return '<tr><td class="%s"%s style="font-family:%s;font-size:%spx;line-height:%s;font-weight:%s;color:%s;padding:%s;%s">%s</td></tr>\n' % (cls, a, FF, size, lh, weight, color, pad, extra, t)

def sparkles():
    s = "".join('<span style="color:%s;font-size:%spx;">&#10022;</span>%s' % (c, z, "&nbsp;&nbsp;") for c, z in ((YELLOW, 13), (PINK, 9), (BLUE, 13), (GREEN, 9), (YELLOW, 13)))
    return '<tr><td align="center" style="font-family:Arial,sans-serif;line-height:1;padding:0 0 14px;">%s</td></tr>\n' % s

def button(label, href, pad="6px 0 4px"):
    return ('<tr><td align="center" style="padding:%s;"><a href="%s" style="display:inline-block;background:%s;color:#ffffff;font-family:%s;'
            'font-size:17px;font-weight:700;text-decoration:none;border-radius:999px;padding:17px 22px;">%s&nbsp;&#8594;</a></td></tr>\n') % (pad, href, CTA, FF, label)

def trust(t):
    parts = ['<span style="white-space:nowrap;">%s</span>' % x for x in t.split(" &middot; ")]
    return text_row(" &middot; ".join(parts), size=13, color=MUTED, cls="muted", pad="9px 0 0", align="center", lh=1.6, extra="text-wrap:balance;")

def card_open(cls="card", bg="#FFFFFF", border="#EFEDE6"):
    return ('<tr><td style="padding:22px 0 0;"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr><td class="%s" bgcolor="%s" '
            'style="background:%s;border:1.5px solid %s;border-radius:22px;padding:24px 22px 20px;"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0">\n') % (cls, bg, bg, border)
CARD_CLOSE = '</table></td></tr></table></td></tr>\n'

def card_h(t):
    return text_row(t, size=19, color=INK, cls="ink", pad="0 0 14px", weight=800, lh=1.25, extra="letter-spacing:-0.3px;")

def dot_item(color, inner, pad="0 0 12px"):
    return ('<tr><td style="padding:%s;"><table role="presentation" cellpadding="0" cellspacing="0" width="100%%"><tr>'
            '<td width="22" valign="top" style="font-family:%s;font-size:15px;line-height:1.6;color:%s;">&#9679;</td>'
            '<td class="body" valign="top" style="font-family:%s;font-size:15.5px;line-height:1.6;color:%s;">%s</td></tr></table></td></tr>\n') % (pad, FF, color, FF, BODY, inner)

def b_ink(t):
    return '<b class="ink" style="color:%s;">%s</b>' % (INK, t)

def build(e, lang, img_base):
    d, c = e[lang], C.COMMON[lang]
    eid = e["id"]; href = link(lang, eid); cta = d.get("cta", c["cta"])
    out = []
    out.append(sparkles())
    out.append('<tr><td align="center" style="font-family:%s;font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:%s;padding:0 0 14px;">%s</td></tr>\n' % (FF, PINK, d["kicker"]))
    out.append('<tr><td class="ink" align="center" style="font-family:%s;font-size:28px;line-height:1.14;font-weight:800;color:%s;letter-spacing:-0.6px;padding:0 0 18px;text-wrap:balance;">%s<br><span class="blue" style="color:%s;">%s</span></td></tr>\n' % (FF, INK, d["h1"], BLUE, d["h1b"]))
    for blk in e["layout"]:
        if blk == "greet":
            g = '{% assign fn = Profile.USER_FIRST_NAME | default: "" %}{% if fn != "" %}' + c["hi"] + '{% else %}' + c["hi0"] + '{% endif %}'
            out.append(text_row(g, pad="30px 0 8px"))
        elif blk == "p":
            letter = "greet" in e["layout"]
            for i, p in enumerate(d["p"]):
                out.append(text_row(p, pad="0 0 %spx" % (4 if (letter and i == len(d["p"]) - 1) else 16 if i == len(d["p"]) - 1 else 12), align=None if letter else "center"))
        elif blk == "hero":
            out.append('<!--HERO--><tr><td align="center" style="padding:0 0 6px;"><img src="%s%s-%s.png" width="600" alt="%s" style="width:100%%;max-width:600px;height:auto;display:block;margin:0 auto;border:0;"></td></tr>\n<!--/HERO-->' % (img_base, eid, lang, H.escape(c["alt"], quote=True)))
        elif blk == "lead":
            out.append(text_row(d["lead"], size=16.5, pad="2px 0 16px", align="center", lh=1.5, extra="text-wrap:balance;"))
        elif blk == "cta":
            out.append(button(cta, href)); out.append(trust(c["trust"]))
        elif blk == "bullets":
            out.append(card_open()); out.append(card_h(d["card_h"]))
            for i, b in enumerate(d["bullets"]): out.append(dot_item(DOTS[i % 4], b, pad="0 0 %spx" % (10 if i < len(d["bullets"]) - 1 else 2)))
            out.append(CARD_CLOSE)
        elif blk == "people":
            out.append(card_open())
            for i, (t, s) in enumerate(d["people"]):
                out.append(dot_item(DOTS[i % 4], b_ink(t) + "<br>" + s, pad="0 0 %spx" % (14 if i < len(d["people"]) - 1 else 2)))
            out.append(CARD_CLOSE)
        elif blk == "steps":
            out.append(card_open())
            for i, (t, s) in enumerate(d["steps"]):
                col = DOTS[i % 4]
                out.append(('<tr><td style="padding:0 0 %spx;"><table role="presentation" cellpadding="0" cellspacing="0" width="100%%"><tr>'
                    '<td width="46" valign="top"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td width="34" height="34" align="center" valign="middle" bgcolor="%s" '
                    'style="background:%s;border-radius:999px;font-family:%s;font-size:16px;font-weight:800;color:#ffffff;line-height:34px;">%s</td></tr></table></td>'
                    '<td class="body" valign="top" style="font-family:%s;font-size:15.5px;line-height:1.55;color:%s;">%s<br>%s</td></tr></table></td></tr>\n')
                    % (16 if i < 2 else 2, col, col, FF, i + 1, FF, BODY, b_ink(t), s))
            out.append(CARD_CLOSE)
        elif blk == "faq":
            out.append(card_open()); out.append(card_h(d["faq_h"]))
            for i, (q, a) in enumerate(d["faq"]):
                last = i == len(d["faq"]) - 1
                out.append('<tr><td class="body hair" style="font-family:%s;font-size:15.5px;line-height:1.6;color:%s;padding:%s;%s">%s<br>%s</td></tr>\n'
                    % (FF, BODY, "12px 0 0" if last else "12px 0 12px", "" if last else "border-bottom:1px solid #EFEDE6;", b_ink(q), a))
            out.append(CARD_CLOSE)
        elif blk == "ask":
            out.append(card_open(cls="tint", bg="#FFF6E3", border="#F7E3B5")); out.append(card_h(d["ask_h"]))
            out.append(text_row(d["ask_p"], size=15.5, pad="0 0 14px", lh=1.6))
            out.append('<tr><td align="center" style="padding:0 0 4px;"><a class="btn2" href="%s" style="display:inline-block;background:transparent;color:%s;font-family:%s;font-size:15.5px;font-weight:700;text-decoration:none;border-radius:999px;border:2px solid %s;padding:13px 20px;">%s&nbsp;&#8594;</a></td></tr>\n'
                % (wa_link(lang, d["wa"]), INK, FF, INK, d["ask_cta"]))
            out.append(CARD_CLOSE)
        elif blk == "close":
            out.append('<tr><td class="ink" align="center" style="font-family:%s;font-size:23px;line-height:1.22;font-weight:800;color:%s;letter-spacing:-0.4px;padding:30px 0 6px;text-wrap:balance;">%s</td></tr>\n' % (FF, INK, d["close_h"]))
            out.append(text_row(d["close_p"], pad="0 0 16px", align="center", lh=1.55))
            out.append(button(cta, href))
            out.append(text_row(c["sign"] + "<br>" + b_ink(c["signer"]), size=15, pad="28px 0 0", lh=1.7))
            out.append(text_row("PS. " + d["ps"], size=13.5, color=MUTED, cls="muted", pad="16px 0 0", lh=1.6))
        elif blk == "close_min":
            out.append(text_row(c["sign"] + "<br>" + b_ink(c["signer"]), size=15, pad="28px 0 0", lh=1.7))
            out.append(text_row("PS. " + d["ps"], size=13.5, color=MUTED, cls="muted", pad="16px 0 0", lh=1.6))
    segs = []
    for chunk in "".join(out).split("<!--HERO-->"):
        if "<!--/HERO-->" in chunk:
            hero_html, rest = chunk.split("<!--/HERO-->", 1)
            segs.append('<table role="presentation" width="100%" cellpadding="0" cellspacing="0">\n' + hero_html + '</table>\n')
            chunk = rest
        if chunk.strip():
            segs.append('<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="padding:0 24px;">\n<table role="presentation" width="100%" cellpadding="0" cellspacing="0">\n' + chunk + '</table>\n</td></tr></table>\n')
    body = "".join(segs)
    if lang == "pt":
        body = body.replace("e-mail", "e&#8209;mail")   # que "e-mail" no se parta al final de un renglon
    return ('<!doctype html>\n<html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">\n<title>%s</title>\n<style>%s</style></head>\n'
        '<body class="bg" style="margin:0;padding:0;background:%s;">\n<div style="display:none;max-height:0;overflow:hidden;">%s</div>\n'
        '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" class="bg" bgcolor="%s" style="background:%s;"><tr><td align="center" style="padding:26px 0 36px;">\n'
        '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%%;"><tr><td>\n'
        '%s</td></tr></table>\n</td></tr></table></body></html>\n'
        ) % ("pt-BR" if lang == "pt" else lang, H.escape(d["subject_a"]), STYLE, BG, H.escape(d["pre"]), BG, BG, body)

def make_hero(e, lang):
    d, c = e[lang], C.COMMON[lang]; h = d["hero"]
    t = dict(chip=H.unescape(c["chip"]), title=c["title"], to_l=c["to_l"], from_l=c["from_l"], to=h["to"], tag_k=h["tag_k"], tag_b=h["tag_b"], tag_s=h["tag_s"])
    t["from"] = h["frm"]
    os.makedirs(IMG_DIR, exist_ok=True)
    out = os.path.join(IMG_DIR, "%s-%s.png" % (e["id"], lang)); raw = out.replace(".png", ".raw.png")
    HERO.render(t, raw)
    # PNG de color completo (la paleta de 256 colores rompia la sombra en anillos); 960 px = 2x a 480 de ancho real en movil
    im = Image.open(raw).convert("RGBA").resize((960, 640), Image.LANCZOS)
    # 6 bits por canal de color y 32 niveles de alfa: baja el peso a la mitad sin bandas visibles
    r, g, bch, al = im.split()
    q6 = lambda v: (v & 0xFC) | 0x02
    im = Image.merge("RGBA", [r.point(q6), g.point(q6), bch.point(q6), al.point(lambda v: (v & 0xF8) | (v >> 5))])
    im.save(out, optimize=True)
    for f in (raw, raw.replace(".png", ".html")):
        if os.path.exists(f): os.remove(f)
    return os.path.getsize(out)

def main():
    local = "--local" in sys.argv; skip_img = "--no-img" in sys.argv
    os.makedirs(OUT, exist_ok=True); n = 0; subjects = []
    for i, e in enumerate(C.EMAILS, 1):
        for lang in e["langs"]:
            if not skip_img:
                kb = make_hero(e, lang) // 1024
            else: kb = os.path.getsize(os.path.join(IMG_DIR, "%s-%s.png" % (e["id"], lang))) // 1024
            html = build(e, lang, IMG_URL)
            assert "—" not in html and "–" not in html, "guion largo en " + e["id"] + lang
            assert html.count("{%") == 4 * (1 if "greet" in e["layout"] else 0) and html.count("{{") == (1 if "greet" in e["layout"] else 0), "llaves Liquid inesperadas en %s %s" % (e["id"], lang)
            name = "GIFT-Holiday-%s-%s-%s.html" % (i if e["id"][0] == "e" else "R", e["id"].split("-", 1)[1], lang.upper())
            open(os.path.join(OUT, name), "w", encoding="utf-8").write(html); n += 1
            if local:
                os.makedirs(os.path.join(OUT, "_preview"), exist_ok=True)
                open(os.path.join(OUT, "_preview", name), "w", encoding="utf-8").write(build(e, lang, "file://" + IMG_DIR + "/"))
            print("%-44s %5.1f KB html · hero %3d KB" % (name, len(html.encode()) / 1024, kb))
    print("listo:", n, "correos en", OUT)

if __name__ == "__main__":
    main()

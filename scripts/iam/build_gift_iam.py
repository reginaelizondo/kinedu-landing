#!/usr/bin/env python3
"""Genera el In-App de Gift para CleverTap (Custom HTML) en EN/ES/PT.

Lecciones de CleverTap que este generador respeta (12-13 oct 2026):
- En el TELEFONO el webview es PANTALLA COMPLETA (el preview de CleverTap engana: ahi la caja se
  encoge al contenido). Por eso .iam lleva min-height:100vh y el fondo pinta toda la pantalla,
  con el contenido centrado y safe-area arriba (la X no tapa el reloj). Todo se mide en vw (ancho, que si es estable), igual que el ejemplo de Solids: asi
  la altura total es predecible y queda en ~130vw (~490 px a 375 de ancho): llena ~75% de la
  pantalla y queda debajo del tope (~84%, medido en el preview).
  Nada en vh (colapsa la caja) ni en px grandes (se desborda).
- Como se mide en vw, en un navegador de escritorio se ve gigante: verlo en el preview de
  CleverTap o en el telefono, no en Chrome de la Mac.
- La tarjeta de regalo se DIBUJA EN CSS (19-oct): sin <img>. La foto del correo (giftcard-*-v4.png,
  tarjeta inclinada y recortada sobre fondo claro) dentro de un marco blanco se veia chueca, cortada
  y con doble marco en el telefono. En CSS queda recta, nitida en retina, igual en claro/oscuro y
  no depende de que CleverTap cargue imagenes externas (su preview las bloquea sin onerror).
- Salida 100% ASCII: acentos y enie como entidades HTML (al pegar en CleverTap salia "√±").
- La X cierra en los dos sistemas: iOS por el puente JS de CleverTap (dismissInAppNotification),
  Android por un href wzrk:// inexistente (el SDK cierra el in-app).
- Boton al web /gift con utm (Gift se compra en web; se lee en /analytics > Gift > Fuentes).
- Marca: Proxima Nova, tinta #2B2E3A, un keyword azul #0086D8 en el titular, fondo calido;
  boton naranja #E57339 por decision de Regina (13-oct).

Uso: python3 scripts/iam/build_gift_iam.py   -> ~/Downloads/gift-iam-clevertap/gift-iam-{EN,ES,PT}.html
"""
import os

OUT = os.path.expanduser("~/Downloads/gift-iam-clevertap")

T = {
 "EN": dict(lang="en", chip="New", h1a="Give a ", kw="year", h1b=" of Kinedu.",
            sub="The gift you wish someone had given you.",
            fb_t="One year of Kinedu", fb_s="Every expert, every class, every milestone.",
            pill="One payment &middot; Nothing renews on them",
            cta="Gift Kinedu now &rarr;", note="Pick the day it arrives. Takes two minutes.",
            url="https://www.kinedu.com/gift?utm_source=inapp&utm_medium=iam&utm_campaign=gift-premium&utm_content=en#no_universal_links",
            tag="Gift card"),
 "ES": dict(lang="es", chip="Nuevo", h1a="Regala un ", kw="año", h1b=" de Kinedu.",
            sub="El regalo que te hubiera encantado recibir.",
            fb_t="Un año de Kinedu", fb_s="Cada experto, cada clase, cada logro.",
            pill="Un solo pago &middot; No se les renueva nada",
            cta="Regala Kinedu ahora &rarr;", note="Elige el día en que llega. Toma dos minutos.",
            url="https://www.kinedu.com/es/gift?utm_source=inapp&utm_medium=iam&utm_campaign=gift-premium&utm_content=es#no_universal_links",
            tag="Tarjeta de regalo"),
 "PT": dict(lang="pt", chip="Novo", h1a="Presenteie um ", kw="ano", h1b=" de Kinedu.",
            sub="O presente que você gostaria de ter recebido.",
            fb_t="Um ano de Kinedu", fb_s="Cada especialista, cada aula, cada conquista.",
            pill="Pagamento único &middot; Nada se renova depois",
            cta="Presenteie Kinedu agora &rarr;", note="Escolha o dia da entrega. Leva dois minutos.",
            url="https://www.kinedu.com/pt/gift?utm_source=inapp&utm_medium=iam&utm_campaign=gift-premium&utm_content=pt#no_universal_links",
            tag="Cartão de presente"),
}

def ent(t):  # todo lo no-ASCII a entidad numerica (las entidades con nombre ya son ASCII)
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in t)

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
<script>
// Android no tiene dark mode en la app: forzamos light ahi.
if (/Android/i.test(navigator.userAgent)) {{ document.documentElement.classList.add('force-light'); }}
</script>
<style>
/* Todo en vw (ancho): la caja de CleverTap mide lo que mide el contenido y tiene tope de
   ~60% de pantalla; con vw la altura total queda en ~93vw y siempre cabe. Nada en vh. */
:root{{
  --bg1:#FCFBF9; --bg2:#F5EFE6;
  --dot-blue:#D5ECFA; --dot-warm:#FEF3DD; --dot-pink:#FBEAF0;
  --ink:#2B2E3A; --body:#5B6170; --muted:#9AA0AD;
  --blue:#0086D8; --orange:#E57339;
  --pillbg:rgba(43,46,58,.05); --pillborder:rgba(43,46,58,.14); --pilltext:#2B2E3A;
  --cardborder:#EFEDE6; --cardbg:#FFFFFF;
  --chipbg:#0086D8; --chiptext:#FFFFFF;
  --ctashadow:rgba(229,115,57,.5);
}}
@media (prefers-color-scheme: dark){{
  :root:not(.force-light){{
    --bg1:#161A26; --bg2:#1F2435;
    --dot-blue:#1F2D3D; --dot-warm:#2A2620; --dot-pink:#2C2230;
    --ink:#F5F6FA; --body:#C7CBD8; --muted:#8A90A0;
    --pillbg:rgba(255,255,255,.08); --pillborder:rgba(255,255,255,.18); --pilltext:#F5F6FA;
    --cardborder:#343949; --cardbg:#262A3C;
    --ctashadow:rgba(229,115,57,.6);
  }}
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:100%;min-height:100%;background:var(--bg1);}}
body{{font-family:'Proxima Nova',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;}}
.iam{{position:relative;width:100%;min-height:100vh;overflow:hidden;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(180deg,var(--bg1) 0%,var(--bg2) 100%);
  padding:max(12vw,calc(env(safe-area-inset-top,0px) + 7vw)) 5vw max(8vw,calc(env(safe-area-inset-bottom,0px) + 6vw));}}
.dot{{position:absolute;z-index:0;border-radius:50%;}}
.d1{{width:38vw;height:38vw;top:-12vw;left:-12vw;background:var(--dot-warm);}}
.d2{{width:24vw;height:24vw;top:18vw;right:-9vw;background:var(--dot-blue);}}
.d3{{width:44vw;height:44vw;bottom:-16vw;right:-15vw;background:var(--dot-blue);}}
.d4{{width:28vw;height:28vw;bottom:10vw;left:-13vw;background:var(--dot-pink);}}
.x{{position:absolute;top:max(10vw,calc(env(safe-area-inset-top,0px) + 3.5vw));right:4vw;z-index:5;width:9vw;height:9vw;border-radius:50%;
  background:var(--pillbg);border:1px solid var(--pillborder);color:var(--ink);display:flex;align-items:center;
  justify-content:center;font-size:6vw;line-height:1;font-weight:700;text-decoration:none;}}
.inner{{position:relative;z-index:1;width:100%;display:flex;flex-direction:column;align-items:center;text-align:center;gap:2.4vw;}}
.chip{{background:var(--chipbg);color:var(--chiptext);font-weight:800;font-size:3.2vw;
  padding:1.6vw 3.8vw;border-radius:999px;letter-spacing:.08em;text-transform:uppercase;}}
h1{{color:var(--ink);font-size:7.2vw;line-height:1.14;font-weight:800;letter-spacing:-.02em;text-wrap:balance;max-width:80vw;}}
h1 .blue{{color:var(--blue);}}
.sub{{color:var(--body);font-size:4vw;font-weight:600;line-height:1.35;max-width:86vw;text-wrap:pretty;}}
/* Tarjeta de regalo dibujada en CSS (recta, nitida, sin imagen). Todo en vw. */
.card{{position:relative;width:70vw;aspect-ratio:1.55;border-radius:3.6vw;overflow:hidden;margin-top:.5vw;color:#fff;text-align:left;
  background:linear-gradient(135deg,#0D93E3 0%,#0086D8 55%,#0A72C4 100%);box-shadow:0 3vw 8vw rgba(43,46,58,.24);}}
.card::before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) .45vw,transparent .6vw);background-size:3vw 3vw;}}
.card::after{{content:"";position:absolute;width:42vw;height:42vw;border-radius:50%;left:-15vw;bottom:-24vw;background:rgba(255,255,255,.08);}}
.cd-logo{{position:absolute;top:3.4vw;left:4vw;z-index:2;display:flex;align-items:center;gap:1.3vw;font-weight:800;font-size:4.4vw;letter-spacing:-.02em;line-height:1;}}
.pw{{display:grid;grid-template-columns:1fr 1fr;gap:.4vw;width:3.6vw;height:3.6vw;}}
.pw i{{display:block;background:#fff;border-radius:.55vw;}}
/* La etiqueta va montada sobre el liston (como en la tarjeta real): asi no choca con el logo ni en PT. */
.cd-tag{{position:absolute;top:3.5vw;right:8.5vw;z-index:2;display:inline-flex;align-items:center;gap:1vw;background:#fff;color:#2B2E3A;
  font-weight:800;font-size:2.1vw;letter-spacing:.06em;text-transform:uppercase;padding:1vw 2.2vw;border-radius:999px;white-space:nowrap;
  box-shadow:0 .6vw 1.8vw rgba(14,54,135,.25);}}
.cd-tag i{{display:block;width:1.6vw;height:1.6vw;border-radius:50%;background:#F9BA48;}}
.cd-rib{{position:absolute;top:0;bottom:0;right:7vw;width:4.6vw;z-index:1;background:linear-gradient(90deg,#F2B13F 0%,#F9BA48 42%,#E8A838 58%,#F9BA48 100%);}}
.cd-txt{{position:absolute;left:4vw;right:14vw;bottom:3.8vw;z-index:2;display:flex;flex-direction:column;}}
.cd-txt b{{font-size:5.6vw;font-weight:800;line-height:1.1;letter-spacing:-.02em;text-wrap:balance;}}
.cd-txt small{{font-size:2.9vw;font-weight:500;opacity:.88;margin-top:1vw;}}
.pill{{display:inline-flex;align-items:center;gap:.5em;background:var(--pillbg);white-space:nowrap;
  border:1px solid var(--pillborder);color:var(--pilltext);font-weight:700;font-size:3.4vw;padding:2.2vw 4vw;border-radius:999px;}}
.cta{{font-weight:800;font-size:5vw;color:#fff;background:var(--orange);border-radius:999px;margin-top:.8vw;
  padding:3.8vw 11vw;text-decoration:none;display:inline-block;animation:pulse 2s infinite;}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 var(--ctashadow)}}70%{{box-shadow:0 0 0 3.5vw rgba(229,115,57,0)}}100%{{box-shadow:0 0 0 0 rgba(229,115,57,0)}}}}
.note{{color:var(--muted);font-size:3vw;font-weight:500;}}
</style></head>
<body><div class="iam">
<a class="x" href="wzrk://dismiss" aria-label="Close" onclick="if(window.webkit&&window.webkit.messageHandlers&&window.webkit.messageHandlers.CleverTap){{window.webkit.messageHandlers.CleverTap.postMessage({{action:'dismissInAppNotification'}});return false;}}">&times;</a>
<div class="dot d1"></div><div class="dot d2"></div><div class="dot d3"></div><div class="dot d4"></div>
<div class="inner">
<span class="chip">&#127873; {chip}</span>
<h1 id="titulo">{h1a}<span class="blue">{kw}</span>{h1b}</h1>
<p class="sub">{sub}</p>
<div class="card">
<div class="cd-logo"><span class="pw"><i></i><i></i><i></i><i></i></span>kinedu</div>
<span class="cd-tag"><i></i>{tag}</span>
<div class="cd-rib"></div>
<div class="cd-txt"><b>{fb_t}</b><small>{fb_s}</small></div>
</div>
<span class="pill">{pill}</span>
<a class="cta" id="cta" href="{url}" data-track="off">{cta}</a>
<p class="note">{note}</p>
</div>
</div>
</body></html>
"""

os.makedirs(OUT, exist_ok=True)
for L, d in T.items():
    html = TEMPLATE.format(**{k: ent(v) for k, v in d.items()})
    assert all(ord(c) < 128 for c in html), L
    p = os.path.join(OUT, f"gift-iam-{L}.html")
    open(p, "w", encoding="utf-8").write(html)
    print("ok", p, len(html), "chars, ASCII")

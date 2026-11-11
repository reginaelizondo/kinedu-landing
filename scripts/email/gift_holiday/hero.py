#!/usr/bin/env python3
"""Renderiza el hero (tarjeta de regalo de temporada) a PNG transparente 2x con Chrome headless."""
import subprocess, sys, os, html
R = "/Users/reginaelizondo/Desktop/CLAUDE/Landing Page"
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

STAR = '<svg class="sp" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({r}deg)" viewBox="0 0 24 24"><path fill="{c}" d="M12 0c.9 6.6 4.5 10.2 12 12-7.5 1.8-11.1 5.4-12 12-.9-6.6-4.5-10.2-12-12C7.5 10.2 11.1 6.6 12 0z"/></svg>'
DOT = '<i class="dot" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></i>'

def page(t):
    sparkles = "".join([
        STAR.format(x=44, y=52, s=30, r=0, c="#F9BA48"), STAR.format(x=508, y=34, s=22, r=12, c="#DA4D7A"),
        STAR.format(x=552, y=176, s=24, r=0, c="#F9BA48"), STAR.format(x=30, y=292, s=18, r=10, c="#45C94E"),
        STAR.format(x=96, y=20, s=14, r=0, c="#32AFE0"), STAR.format(x=470, y=356, s=16, r=0, c="#32AFE0"),
        DOT.format(x=22, y=180, s=9, c="#DA4D7A"), DOT.format(x=566, y=140, s=8, c="#45C94E"),
        DOT.format(x=150, y=372, s=7, c="#F9BA48"), DOT.format(x=420, y=14, s=7, c="#F9BA48"),
        DOT.format(x=560, y=330, s=6, c="#DA4D7A"), DOT.format(x=52, y=236, s=6, c="#32AFE0"),
    ])
    e = html.escape
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:PN;src:url('file://{R}/fonts/proxima-nova/proximanova-regular-webfont.woff2') format('woff2');font-weight:400}}
@font-face{{font-family:PN;src:url('file://{R}/fonts/proxima-nova/proximanova-bold-webfont.woff2') format('woff2');font-weight:700}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:600px;height:400px;background:transparent;font-family:PN,'Avenir Next',Helvetica,Arial,sans-serif;overflow:hidden}}
.stage{{position:absolute;left:0;top:0;width:600px;height:400px}}
.sp,.dot{{position:absolute}} .dot{{border-radius:50%;display:block}}
.card{{position:absolute;left:78px;top:70px;width:432px;height:266px;border-radius:24px;transform:rotate(-4deg);
  background:linear-gradient(135deg,#1FA2EA 0%,#0086D8 46%,#0A6FC0 100%);
  box-shadow:0 18px 30px rgba(8,27,70,.22),0 4px 10px rgba(8,27,70,.14);overflow:hidden;color:#fff}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.17) 1.4px,transparent 1.6px);background-size:18px 18px}}
.blob{{position:absolute;width:250px;height:250px;left:-96px;bottom:-124px;border-radius:50%;background:rgba(255,255,255,.10)}}
.gloss{{position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.26) 0%,rgba(255,255,255,0) 40%)}}
.rv{{position:absolute;top:0;bottom:0;right:78px;width:40px;background:linear-gradient(90deg,#F4AE33,#FBC55C 45%,#F4AE33);box-shadow:-8px 0 18px rgba(0,0,0,.10),8px 0 18px rgba(0,0,0,.07)}}
.rh{{position:absolute;left:0;right:0;top:150px;height:0}}
.logo{{position:absolute;left:28px;top:27px;height:24px}}
.chip{{position:absolute;right:136px;top:28px;background:#fff;color:#2B2E3A;font-size:{'8.4px' if len(t['chip'])>10 else '9.5px'};font-weight:700;letter-spacing:{'.08em' if len(t['chip'])>10 else '.14em'};text-transform:uppercase;padding:6px 10px 6px 9px;border-radius:999px;white-space:nowrap}}
.chip i{{display:inline-block;width:6px;height:6px;border-radius:50%;background:#F9BA48;margin-right:6px;vertical-align:middle;position:relative;top:-1px}}
.title{{position:absolute;left:28px;top:88px;font-size:33px;font-weight:700;letter-spacing:-.02em;line-height:1.06;max-width:290px}}
.sub{{position:absolute;left:28px;top:{t.get('subtop',144)}px;font-size:12.5px;line-height:1.4;color:#D5ECFA;max-width:262px}}
.meta{{position:absolute;left:28px;bottom:26px;border-collapse:collapse}}
.meta td{{font-size:14.5px;color:#fff;padding:2px 0;white-space:nowrap;vertical-align:baseline}}
.meta td.l{{font-weight:700;color:#D5ECFA;font-size:10px;letter-spacing:.14em;text-transform:uppercase;padding-right:12px}}
/* moño */
.bow{{position:absolute;left:356px;top:36px;width:150px;height:110px;transform:rotate(-4deg)}}
/* etiqueta colgante */
.tag{{position:absolute;left:{t.get('tagx',378)}px;top:222px;transform:rotate(6deg);background:#FFFDF8;border-radius:15px;padding:14px 17px 13px 17px;box-shadow:0 14px 26px rgba(8,27,70,.22),0 2px 6px rgba(8,27,70,.12);min-width:150px}}
.tag:before{{content:"";position:absolute;left:16px;top:-9px;width:12px;height:12px;border-radius:50%;background:#FFFDF8;border:3px solid #E9E2D3}}
.tag small{{display:block;font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#DA4D7A;margin-bottom:3px;white-space:nowrap}}
.tag b{{display:block;font-size:20.5px;font-weight:700;color:#2B2E3A;letter-spacing:-.01em;white-space:nowrap;line-height:1.15}}
.tag span{{display:block;font-size:12.5px;color:#5B6170;margin-top:2px;white-space:nowrap}}
.string{{position:absolute;left:0;top:0;width:600px;height:400px;pointer-events:none}}
</style></head><body><div class="stage">
{sparkles}
<div class="card"><span class="dots"></span><span class="blob"></span><span class="gloss"></span><span class="rv"></span>
  <img class="logo" src="file://{R}/kinedu-logo-white.png" alt="">
  <span class="chip"><i></i>{e(t['chip'])}</span>
  <div class="title">{t['title']}</div>
  <table class="meta"><tr><td class="l">{e(t['to_l'])}</td><td>{e(t['to'])}</td></tr><tr><td class="l">{e(t['from_l'])}</td><td>{e(t['from'])}</td></tr></table>
</div>
<svg class="string" viewBox="0 0 600 400"><path d="M431 118 C 440 158, 412 190, 401 220" fill="none" stroke="#E9E2D3" stroke-width="2.2" stroke-linecap="round"/></svg>
<svg class="bow" viewBox="0 0 150 110">
  <path d="M75 56 C 52 18, 16 14, 12 38 C 9 58, 44 66, 75 56 Z" fill="#F9BA48"/>
  <path d="M75 56 C 98 18, 134 14, 138 38 C 141 58, 106 66, 75 56 Z" fill="#FBC55C"/>
  <path d="M75 56 C 58 34, 34 30, 28 42 C 26 52, 50 58, 75 56 Z" fill="#E59E1E" opacity=".55"/>
  <path d="M75 56 C 92 34, 116 30, 122 42 C 124 52, 100 58, 75 56 Z" fill="#E59E1E" opacity=".45"/>
  <path d="M70 58 L 50 100 L 62 96 L 68 106 L 78 60 Z" fill="#F4AE33"/>
  <path d="M80 58 L 100 100 L 88 96 L 82 106 L 72 60 Z" fill="#F9BA48"/>
  <rect x="64" y="45" width="22" height="22" rx="7" fill="#F4AE33"/><rect x="67" y="48" width="16" height="16" rx="5" fill="#FBC55C"/>
</svg>
<div class="tag"><small>{e(t['tag_k'])}</small><b>{e(t['tag_b'])}</b><span>{e(t['tag_s'])}</span></div>
</div></body></html>"""

def render(t, out):
    h = out.replace(".png", ".html"); open(h, "w", encoding="utf-8").write(page(t))
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", f"--user-data-dir=/tmp/chrome-hero",
        "--force-device-scale-factor=2", "--window-size=600,400", "--default-background-color=00000000", "--virtual-time-budget=3000",
        f"--screenshot={out}", "file://" + h], capture_output=True)
    return os.path.getsize(out)

if __name__ == "__main__":
    t = dict(chip="Gift card", title="One year<br>of Kinedu", sub="Every expert, every class, every milestone. All unlocked.", subtop=176,
             to_l="To", to="Sarah & baby Emma", from_l="From", **{"from": "Grandma Rosa"}, tag_k="Arrives", tag_b="Dec 25 · 7:00 AM", tag_s="Scheduled by you")
    print(render(t, sys.argv[1]))

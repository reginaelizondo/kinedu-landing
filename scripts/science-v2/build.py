# -*- coding: utf-8 -*-
"""Construye las 3 páginas de Science (EN) a partir del shell de science.html
   + el guion de Luis + el libro Big Bang Baby. Sin guiones largos en copy."""
import re, os, json
L=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
src=open(os.path.join(os.path.dirname(__file__),"science.orig.html"),encoding="utf-8").read()
lines=src.split("\n")
def block(a,b): return "\n".join(lines[a-1:b])

HEAD=src[:src.index("</head>")]
HEAD=re.sub(r'\s*<link rel="preconnect" href="https://fonts\.g[^"]*"[^>]*>', '', HEAD)
HEAD=re.sub(r'\s*<link href="https://fonts\.googleapis\.com/css2[^>]*>', '', HEAD)
HEAD=HEAD.replace("font-family: 'Plus Jakarta Sans', sans-serif;", "font-family: 'Proxima Nova', sans-serif;")
assert "Plus Jakarta" not in HEAD and "googleapis" not in HEAD
NAV=block(1005,1049)
FOOTER=block(1393,1431)
FOOTER=FOOTER.replace('<a href="/science" data-i18n="footer.theScience">The science</a>', '<a href="/science" data-i18n="footer.theScience">The science</a>\n                    <a href="/gift" data-i18n="footer.gift" data-i18n-href="footer.giftUrl">Gift Kinedu</a>',1)
assert 'footer.gift' in FOOTER
FOOTER=re.sub(r'(<a[^>]*aria-label="[^"]*"[^>]*>\s*<svg)(?![^>]*aria-hidden)', r'\1 aria-hidden="true"', FOOTER)
TAIL=block(1433,1475).replace("?v=0843a","?v=0844a")   # translations/script + track (sin el script de paneles ni el reveal muerto)
TAIL=TAIL.replace('a[href*="app.kinedu.com"]', 'a[href*="app.kinedu.com"], a[href*="webpromo.kinedu.com"], a[href*="/assessment"]')
TAIL=re.sub(r"\s*<script>\s*\(function\(\)\{\s*var sel='\.science-section-header.*?</script>", "", TAIL, flags=re.S)
assert "science-section-header" not in TAIL and 'webpromo.kinedu.com"]' in TAIL

# fragmentos reutilizables (gráficas ya existentes)
SCIQ=block(1197,1233)+"\n</script>"
for _a,_b in [("49.5% of 12-month-olds show it · asked right where new skills are appearing, which is where an answer teaches us something","In our data, caregivers reported this skill in 49.5% of 12-month-olds."),("“Can stand up from a squat all alone.”","Can your baby stand up from a squat without help?"),("“Pushes a button or flips a switch to make something happen.”","Does your baby push a button or flip a switch to make something happen?"),("“Waves bye-bye when someone waves first.”","Does your baby wave bye-bye when someone waves first?"),
              ("thinking you can literally watch · every question is a behavior, never a judgment","Cognitive questions look at how your baby explores and solves problems."),
              ("connection shows up in tiny gestures · either answer is information","Social-emotional questions look at how your baby connects with people."),
              ("Example, not a real child's result.","This is an example, not an individual child’s result."),("That's the whole gesture.","That’s it."),("32 questions like these, less than 5 minutes, adapted to your child's age. Either answer teaches the map something.","32 questions like these, in about 5 minutes, adapted to your child’s age."),
              ('q.note + " \\u00b7 " + CFG.disclaimer', 'q.note + " " + CFG.disclaimer')]:
    assert _a in SCIQ, _a
    SCIQ=SCIQ.replace(_a,_b)          # widget de preguntas (cierra el script que abre en 1198)
CH_HEAD=re.search(r'<div class="sci26-chart"><svg viewBox="0 0 380 210".*?</div>', block(1242,1242), re.S).group(0).replace('“Lifts head while on tummy”: share of babies showing it, by age · Kinedu record, 2020–2023. This curve is what turns a “yes” into information.','“Lifts head while on tummy”: share of caregivers reporting it, by age, across the Kinedu population · Kinedu record, 2020–2023 · a population pattern, not an individual baby’s path')
CH_BABBLE=re.sub(r' data-i18n="cur\.[a-z_]+"', "", block(1244,1245)).replace("Babbling hands off to first words.","From babbling to first words.").replace("Babbling builds early: half of children by 5 months. As children move toward first words, the assessment shifts its attention from babbling to early speech.","As children develop early speech, the assessment shifts its focus from babbling to words.").replace("Share of children showing each skill, by age · Kinedu record, 2020–2023 · shaded band ±1 SD across the skill's milestones","Average share of “yes” answers across the milestones in each skill group, by age · Kinedu record, 2020–2023 · shaded band ±1 SD")
CH_WALK=re.sub(r' data-i18n="cur\.[a-z_]+"', "", block(1246,1247)).replace("Walking arrives, and stays.","From first steps to more confident movement.").replace("Half of children by 19 months, three quarters by 29, and once gained, never handed off. The wide range is real: children reach it at genuinely different ages.", "This skill group includes several milestones, from taking first steps to more advanced movement.").replace("Share of children showing the skill, by age · Kinedu record, 2020–2023","Average share of “yes” answers across the milestones in this skill group, by age · Kinedu record, 2020–2023")                 # div.sci26-chart abierto en 1244 y cerrado al final de 1245
CH_FAN=re.search(r'<div class="pg-one">.*?</div></div></div>', block(1351,1351), re.S).group(0)
SEQ=block(1355,1356)
for _a,_b in [("≈ 2 m<","≈ 3 mo<"),("≈ 6 m<","≈ 7 mo<"),("≈ 9 m<","≈ 12 mo<"),("≈ 12 m<","≈ 13 mo<")]:
    assert _a in SEQ, _a
    SEQ=SEQ.replace(_a,_b)
DISP=block(1360,1361)
for _a,_b in [
 ('<rect x="477" y="46" width="135" height="34" rx="17" fill="#3EB646"/><text x="545" y="68" text-anchor="middle" font-size="12.5" fill="#fff" font-weight="800" font-family="Proxima Nova,Arial">8–13 m · a 5-month range</text>',
  '<rect x="385" y="46" width="77" height="34" rx="17" fill="#3EB646"/><text x="474" y="68" font-size="12.5" fill="#33415C" font-weight="700" font-family="Proxima Nova,Arial">8–13 mo · a 5-month range</text>'),
 ('<rect x="316" y="118" width="592" height="34" rx="17" fill="#F99848"/><text x="612" y="140" text-anchor="middle" font-size="12.5" fill="#fff" font-weight="800" font-family="Proxima Nova,Arial">2–24 m · a 22-month range</text>',
  '<rect x="523" y="118" width="338" height="34" rx="17" fill="#F99848"/><text x="692" y="140" text-anchor="middle" font-size="12.5" fill="#fff" font-weight="800" font-family="Proxima Nova,Arial">17–39 mo · a 22-month range</text>'),
 ('<circle cx="424" cy="176" r="3" fill="#D9D2C7"/><text x="424" y="200" text-anchor="middle" font-size="11.5" fill="#8A94A8" font-family="DM Mono,monospace">6</text><circle cx="585" cy="176" r="3" fill="#D9D2C7"/><text x="585" y="200" text-anchor="middle" font-size="11.5" fill="#8A94A8" font-family="DM Mono,monospace">12</text><circle cx="746" cy="176" r="3" fill="#D9D2C7"/><text x="746" y="200" text-anchor="middle" font-size="11.5" fill="#8A94A8" font-family="DM Mono,monospace">18</text><circle cx="908" cy="176" r="3" fill="#D9D2C7"/><text x="908" y="200" text-anchor="middle" font-size="11.5" fill="#8A94A8" font-family="DM Mono,monospace">24 months</text>',
  ''.join('<circle cx="%d" cy="176" r="3" fill="#D9D2C7"/><text x="%d" y="200" text-anchor="middle" font-size="11.5" fill="#8A94A8" font-family="DM Mono,monospace">%s</text>'%(262+round(m*15.381),262+round(m*15.381),(str(m) if m<42 else "42 months")) for m in (6,12,18,24,30,36,42))),
 ('<span class="rng">8–13 m</span></div><div class="track"><div class="bar" style="left:33.3%;width:20.8%;background:#3EB646"></div>',
  '<span class="rng">8–13 mo · 5 months wide</span></div><div class="track"><div class="bar" style="left:19%;width:11.9%;background:#3EB646"></div>'),
 ('<span class="rng">2–24 m</span></div><div class="track"><div class="bar" style="left:8.3%;width:91.7%;background:#F99848"></div>',
  '<span class="rng">17–39 mo · 22 months wide</span></div><div class="track"><div class="bar" style="left:40.5%;width:52.4%;background:#F99848"></div>'),
 ('<div class="pg-maxis"><span>0</span><span>12</span><span>24 months</span></div>', '<div class="pg-maxis"><span>0</span><span>21</span><span>42 months</span></div>'),
]:
    assert _a in DISP, _a[:60]
    DISP=DISP.replace(_a,_b)
WIN=block(1366,1367)
PG_CSS=block(1278,1342)
_PRON=[(">Social<",">Social-emotional<"),("Now they can study the whole room","A new view of the room"),("Now they can turn toward your voice","More ways to respond to your voice"),("Now they can hold your gaze","More opportunities for face-to-face interaction"),("…that one skill opens three more doors:","…and that one skill opens new possibilities:"),("Dressing &amp; feeding themselves","Dressing and feeding themselves"),("Dressing & feeding themselves","Dressing and feeding themselves")]
for _a,_b in _PRON:
    CH_FAN=CH_FAN.replace(_a,_b); SEQ=SEQ.replace(_a,_b); DISP=DISP.replace(_a,_b)
SCI26_CSS=block(1105,1194)+"\n</style>"

# ---------- helpers ----------
def head(title, desc, path, og_title=None):
    h=HEAD
    h=re.sub(r"<title>.*?</title>", "<title>%s</title>"%title, h, count=1)
    h=re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">'%desc, h, count=1)
    h=re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://www.kinedu.com%s">'%path, h, count=1)
    if path!="/science":
        h=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', h)
        h=h.replace('<link rel="canonical"', '<link rel="alternate" hreflang="en" href="https://www.kinedu.com%s">\n<link rel="alternate" hreflang="es" href="https://www.kinedu.com/es%s">\n<link rel="alternate" hreflang="pt" href="https://www.kinedu.com/pt%s">\n<link rel="alternate" hreflang="x-default" href="https://www.kinedu.com%s">\n<link rel="canonical"'%(path,path,path,path),1)
    for k in ("og:title","twitter:title"):
        h=re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*'%k, r'\g<1>'+(og_title or title), h)
    for k in ("og:description","twitter:description"):
        h=re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*'%k, r'\g<1>'+desc, h)
    h=re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>https://www.kinedu.com'+path, h)
    h=re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>https://www.kinedu.com/og-'+path.strip('/')+'.png', h)
    crumbs=[{"@type":"ListItem","position":i+1,"name":t,"item":"https://www.kinedu.com"+pp} for i,(pp,t) in enumerate(NAV_ITEMS) if pp==path or i==0]
    if path!="/science": crumbs=[crumbs[0], {"@type":"ListItem","position":2,"name":dict(NAV_ITEMS)[path],"item":"https://www.kinedu.com"+path}]
    ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumbs},ensure_ascii=False)+'</script>\n'
    return h+ld

NAV_ITEMS=[("/science","How Kinedu was built"),("/science-what-we-know","How babies grow"),("/science-what-you-can-do","What you can do as a parent")]
def nav(active):
    n=NAV
    items="".join('<a href="%s" class="nd-item%s" role="menuitem"><span>%s</span></a>'%(p," is-active" if p==active else "",t) for p,t in NAV_ITEMS)
    n=re.sub(r'<a href="/science" class="nd-item" role="menuitem"><span>[^<]*</span></a>\s*<a href="/science#assessment" class="nd-item" role="menuitem"><span>[^<]*</span></a>', items, n)
    classes=('<div class="nav-dropdown" id="classesDropdown"><button class="nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true"><span data-i18n="nav.classes">Classes</span>'
             '<svg class="nav-chevron" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
             '<div class="nav-dropdown-menu" role="menu"><a href="/masterclasses" class="nd-item" role="menuitem"><span data-i18n="nav.masterclasses">Masterclasses</span></a>'
             '<a href="/live-classes" class="nd-item" role="menuitem"><span data-i18n="nav.liveClasses">Live Classes</span></a></div></div>')
    n=re.sub(r'<a href="/masterclasses" data-i18n="nav.masterclasses">Masterclasses</a>\s*<a href="/live-classes" data-i18n="nav.liveClasses">Live Classes</a>', classes, n, count=1)
    assert 'data-i18n="nav.classes"' in n
    return n

def chapters(active):
    pills=[]
    for i,(p,t) in enumerate(NAV_ITEMS,1):
        cls=' class="on"' if p==active else ''
        pills.append('<a href="%s"%s><span class="n">%d</span>%s</a>'%(p,cls,i,t))
    return '<nav class="sci-chapters" aria-label="The science, in three parts"><div class="sci-chapters-in"><span class="lbl">The science, in three parts</span>'+"".join(pills)+'</div></nav>'

def cta(text, href, primary=True, extra=""):
    if primary:
        return '<a href="%s" class="sci-btn sci-btn-primary"%s>%s</a>'%(href,extra,text)
    return '<a href="%s" class="sci-btn sci-btn-ghost"%s>%s</a>'%(href,extra,text)

TRY="https://webpromo.kinedu.com/p/landing-kinedu"
ASSESS="https://www.kinedu.com/assessment"

COMMON_CSS = """
<style>
/* ── Science v2 (3 partes) ── */
.sci-chapters{background:#FBFAF8;border-bottom:1px solid #EEE9E1}
.sci-chapters-in{max-width:1040px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:center}
.sci-chapters .lbl{font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8A94A8;margin-right:6px}
.sci-chapters a{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:#fff;border:1.5px solid #EBE6DF;font-weight:700;font-size:13.5px;color:#081B46;text-decoration:none;transition:border-color .15s,color .15s}
.sci-chapters a:hover{border-color:#087BF3;color:#087BF3}
.sci-chapters a.on{background:#081B46;border-color:#081B46;color:#fff}
.sci-chapters a .n{width:20px;height:20px;border-radius:99px;background:#EFF4FB;color:#087BF3;font-size:11.5px;font-weight:800;display:inline-flex;align-items:center;justify-content:center}
.sci-chapters a.on .n{background:rgba(255,255,255,.18);color:#fff}
.sci-hero-kick{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#087BF3;background:#EFF4FB;border:1px solid #D6E6FB;padding:8px 18px;border-radius:999px;margin:0 auto 18px}
.science-hero h1{max-width:900px;margin-left:auto;margin-right:auto;text-wrap:balance}
.science-hero .hero-sub{margin-left:auto;margin-right:auto}
.sci-hero-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.sci-btn{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:15px 30px;font-weight:800;font-size:15.5px;text-decoration:none;transition:transform .15s,box-shadow .15s}
.sci-btn-primary{background:#087BF3;color:#fff;box-shadow:0 14px 30px -12px rgba(8,123,243,.6)}
.sci-btn-primary:hover{transform:translateY(-2px)}
.sci-btn-ghost{background:#fff;color:#081B46;border:1.5px solid #D9DFEA}
.sci-btn-xl{padding:20px 40px;font-size:18px;background:linear-gradient(135deg,#2B96FF,#087BF3 60%,#0B6BD0);box-shadow:0 22px 44px -16px rgba(8,123,243,.65),0 0 0 8px rgba(8,123,243,.08)}
.sci-btn-xl .arr{display:inline-block;transition:transform .15s}
.sci-btn-xl:hover .arr{transform:translateX(4px)}
.sci-btn-note{margin:14px 0 0;font-size:13.5px;color:#8A94A8}
.sci-btn-ghost:hover{border-color:#087BF3;color:#087BF3}
.sci-prose{max-width:760px;margin:0 auto;text-align:left}
.sci-prose p{font-size:17.5px;line-height:1.7;color:#33415C;margin:0 0 18px;text-wrap:pretty}
.sci-prose p strong{color:#081B46}
.sci-prose p.big{font-size:clamp(21px,2.6vw,27px);font-weight:700;line-height:1.35;color:#081B46;letter-spacing:-.02em;margin:26px 0 22px}
.sci-cases{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:26px auto 0;max-width:1040px}
.sci-case{background:#fff;border:1px solid #EBE6DF;border-radius:18px;padding:22px 22px;font-size:15.5px;line-height:1.55;color:#33415C}
.sci-case b{display:block;color:#081B46;font-size:17px;line-height:1.3;letter-spacing:-.01em;margin-bottom:8px}
.sci-states{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:26px auto 0;max-width:1040px}
.sci-state{border-radius:18px;padding:20px 18px;background:#fff;border:1px solid #EBE6DF}
.sci-state .dot{width:12px;height:12px;border-radius:99px;display:inline-block;margin-bottom:10px}
.sci-state b{display:block;font-size:16px;color:#081B46;margin-bottom:4px}
.sci-state p{margin:0;font-size:14px;line-height:1.5;color:#52607A}
.sci-emerge{display:flex;align-items:stretch;gap:10px;justify-content:center;flex-wrap:wrap;margin:26px auto 0;max-width:1040px}
.sci-emerge .st{flex:1 1 200px;background:#fff;border:1px solid #EBE6DF;border-radius:16px;padding:16px 18px;position:relative}
.sci-emerge .st .k{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8A94A8;margin-bottom:6px}
.sci-emerge .st b{font-size:15.5px;color:#081B46}
.sci-emerge .st::after{content:'→';position:absolute;right:-13px;top:50%;transform:translateY(-50%);color:#C9D2E0;font-weight:800;font-size:18px}
.sci-emerge .st:last-child::after{content:none}
.sci-emerge .st:last-child{border-color:#087BF3;box-shadow:0 12px 28px -14px rgba(8,123,243,.5)}
.sci-quote{font-size:clamp(24px,3.6vw,36px);font-weight:800;letter-spacing:-.03em;line-height:1.2;color:#081B46;text-align:center;max-width:880px;margin:36px auto 0}
.sci-quote .mk{background:linear-gradient(transparent 58%,rgba(255,189,21,.38) 58%)}
.sci-honest{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:26px auto 0;max-width:1040px}
.sci-honest .c{background:#fff;border:1px solid #EBE6DF;border-radius:18px;padding:22px}
.sci-honest .c b{display:block;font-size:16px;color:#081B46;margin-bottom:6px}
.sci-honest .c p{margin:0;font-size:14.5px;line-height:1.55;color:#52607A}
.sci-proof{display:flex;gap:12px;align-items:flex-start;max-width:860px;margin:22px auto 0;background:#fff;border:1.5px solid #EBE6DF;border-radius:16px;padding:16px 20px;text-align:left}
.sci-proof .tag{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#fff;background:#081B46;border-radius:999px;padding:5px 10px;flex-shrink:0;margin-top:2px}
.sci-proof p{margin:0;font-size:15px;line-height:1.55;color:#33415C}
.sci-next{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;max-width:1040px;margin:0 auto}
.sci-next a{text-decoration:none;font-weight:800;color:#087BF3;font-size:15.5px}
.sci-next .prev{color:#8A94A8}
.sci-app{display:flex;align-items:center;gap:18px;background:linear-gradient(135deg,#fff,#F4F8FF);border:1.5px solid #D6E6FB;border-radius:20px;padding:20px 22px;margin-top:26px;position:relative;text-decoration:none;color:inherit;text-align:left;transition:transform .15s,box-shadow .15s,border-color .15s}
.sci-app:hover{transform:translateY(-2px);border-color:#087BF3;box-shadow:0 18px 40px -20px rgba(8,123,243,.45)}
.sci-app img{width:52px;height:52px;border-radius:14px;flex-shrink:0;box-shadow:0 6px 16px rgba(8,27,70,.12)}
.sci-app .body{flex:1;min-width:0}
.sci-app .k{display:block;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#087BF3;margin-bottom:4px}
.sci-app b{display:block;font-size:17px;color:#081B46;line-height:1.25;margin-bottom:4px}
.sci-app p{margin:0;font-size:14.5px;line-height:1.5;color:#52607A}
.sci-app .go{flex-shrink:0;font-weight:800;font-size:14.5px;color:#087BF3;white-space:nowrap}
.sci-datatag{position:absolute;z-index:2;top:-10px;left:50%;transform:translateX(-50%);font-size:10.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#7A5B00;background:#FFE9A8;border-radius:999px;padding:4px 10px;white-space:nowrap}
.sci-app .draft{position:absolute;top:-11px;right:16px;font-size:10.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#7A5B00;background:#FFE9A8;border-radius:999px;padding:4px 10px}
@media(max-width:640px){.sci-app{flex-wrap:wrap}.sci-app .go{width:100%;padding-left:70px}}
.sci-stress{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:26px auto 0;max-width:1040px}
.sci-stress .c{border-radius:18px;padding:22px}
.sci-stress .c b{display:block;font-size:17px;color:#081B46;margin-bottom:6px}
.sci-stress .c p{margin:0;font-size:14.5px;line-height:1.55;color:#33415C}
.sci-spectrum{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:26px auto 0;max-width:1040px}
.sci-spectrum .c{background:#fff;border:1px solid #EBE6DF;border-radius:16px;padding:18px}
.sci-spectrum .c .lbl{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8A94A8;margin-bottom:6px}
.sci-spectrum .c b{display:block;font-size:15.5px;color:#081B46;margin-bottom:4px}
.sci-spectrum .c p{margin:0;font-size:13.5px;line-height:1.5;color:#52607A}
.sci-mantra{font-weight:800;font-size:clamp(24px,3.6vw,38px);letter-spacing:-.02em;color:#081B46;text-align:center;margin:30px 0 0;word-spacing:.18em}
.sci-onepct{max-width:640px;margin:26px auto 0}
.sci-onepct .track{height:34px;border-radius:17px;background:#F1EFE9;position:relative;overflow:hidden}
.sci-onepct .fill{position:absolute;left:0;top:0;bottom:0;width:1.5%;min-width:6px;background:#087BF3;border-radius:17px}
.sci-onepct .lab{display:flex;justify-content:space-between;font-size:13px;color:#52607A;margin-top:10px}
.sci-onepct .lab b{color:#087BF3}
.sci-fade{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:860px;margin:22px auto 0}
.sci-fade .c{background:#fff;border:1px solid #EBE6DF;border-radius:16px;padding:16px 18px;text-align:center}
.sci-fade .c .v{font-weight:800;font-size:24px;letter-spacing:-.02em;color:#081B46}
.sci-fade .c p{margin:6px 0 0;font-size:13px;color:#52607A;line-height:1.45}
@media(max-width:900px){.sci-cases,.sci-honest,.sci-stress{grid-template-columns:1fr}.sci-states,.sci-spectrum{grid-template-columns:1fr 1fr}.sci-fade{grid-template-columns:1fr}}
@media(max-width:560px){.sci-hero-kick{font-size:11px;padding:7px 14px;letter-spacing:.08em}.sci-states,.sci-spectrum{grid-template-columns:1fr}.sci-emerge .st::after{content:none}.sci-prose p{font-size:16.5px}}
.science-hero{padding-bottom:44px!important}
.sci26-plain::before,.sci26-plain::after{display:none!important}
</style>
"""

def hero(kick, h1, sub, ctas, badges=True):
    b = ""
    return """    <section class="science-hero">
        <div class="section-wrap">
            <div class="sci-hero-kick">%s</div>
            <h1>%s</h1>
            <p class="hero-sub">%s</p>
%s%s
        </div>
    </section>""" % (kick, h1, sub, ('<div class="sci-hero-ctas">%s</div>' % ctas) if ctas else "", b)

def sec(kick, h2, lead, body, accent="#087BF3", cls="", maxw=1040, extra_style=""):
    lead_html = '<p class="sci26-lead">%s</p>'%lead if lead else ""
    return '<section class="sci26 %s" style="--sciacc:%s;%s"><div class="sci26-wrap" style="max-width:%dpx"><div class="sci26-kick">%s</div><h2>%s</h2>%s%s</div></section>' % (cls, accent, extra_style, maxw, kick, h2, lead_html, body)

CAN=[("Show which skills your baby is developing","and what usually comes next."),
     ("Help you prepare questions","for your child’s healthcare professional."),
     ("Put your observations in context","using patterns from other children’s development.")]
CANNOT=[("Provide a diagnosis.","The assessment supports conversations with a qualified healthcare professional."),
        ("Evaluate your parenting.","These data describe children’s skills, not the care they receive."),
        ("Represent every family.","The findings come from families who chose to use Kinedu.")]
def honest(items=None, kick="What the results mean", h2='What the assessment can tell you, <span class="sci-squig">and what it can’t.</span>', cls="sci26-blue", accent="#0E3687", tail="", cannot=None):
    cannot=cannot or CANNOT
    col=lambda title,icon,rows,cls2: '<div class="sci-cc %s"><div class="h"><span class="i">%s</span>%s</div>'%(cls2,icon,title)+"".join('<div class="r"><b>%s</b> %s</div>'%(b,p) for b,p in rows)+'</div>'
    body='<div class="sci-cancan">'+col("What it can do","✓",CAN,"can")+col("What it cannot do","✕",cannot,"cannot")+'</div>'
    return sec(kick, h2, "", body+tail, accent, cls)

DOC_ICON='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 15h6M9 11h2"/></svg>'
READ_WORK = """<div class="sci-docs">
<a href="/research/kinedu-replication-EXTERNAL.pdf" class="sci-doc">"""+DOC_ICON+"""<span>Research report<small>PDF · full methods and figures</small></span></a>
<a href="/research/kinedu-parents-guide.pdf" class="sci-doc">"""+DOC_ICON+"""<span>Parent’s guide<small>PDF · the findings in plain language</small></span></a>
</div>
<p style="font-family:'DM Mono',monospace;font-size:11.5px;color:#8A94A8;margin-top:18px;text-align:center">Coupling and Differentiation in Early Development · July 2026 · Kinedu supports developmental surveillance. It is not a diagnosis.</p>"""

def nextprev(prev, nxt):
    p='<a class="prev" href="%s">← %s</a>'%prev if prev else "<span></span>"
    n='<a href="%s">Next: %s →</a>'%nxt if nxt else ""
    return '<section class="sci26 sci26-plain" style="padding:26px 20px 40px"><div class="sci-next">%s%s</div></section>'%(p,n)

def page(path, title, desc, active, hero_html, sections, og_title=None):
    return (head(title, desc, path, og_title) + COMMON_CSS + "</head>\n<body>\n" + nav(active) + "\n" + hero_html + "\n" + chapters(active) + "\n" + SCI26_CSS + "\n" + PG_CSS + "\n" + "\n".join(sections) + "\n<!-- FOOTER -->\n" + FOOTER + "\n\n" + TAIL + "\n</body>\n</html>\n")

p3_note = '<section class="sci26 sci26-plain" style="padding:10px 20px 30px"><div class="sci26-wrap" style="max-width:860px"><p style="font-family:\'DM Mono\',monospace;font-size:11.5px;color:#8A94A8;text-align:center;line-height:1.7">References to Stanford, Harvard’s Center on the Developing Child and named researchers are for attribution only and do not imply endorsement of Kinedu. Nothing on this page is medical advice.</p></div></section>'

COUPLING_SVG = """<div class="sci26-chart" style="max-width:520px"><h3 style="font-size:19px;font-weight:800;color:#081B46;margin:0 0 8px">The four areas become more distinct as children grow.</h3>
<p style="font-size:14.5px;color:#52607A;line-height:1.6;margin:0 0 16px">Following the same children from 2 to 35 months.</p>
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" role="img" font-family="DM Sans,Arial,sans-serif">
<line x1="56" y1="214" x2="500" y2="214" stroke="#E7E2D8"/><line x1="56" y1="152" x2="500" y2="152" stroke="#E7E2D8"/><line x1="56" y1="90" x2="500" y2="90" stroke="#E7E2D8"/><line x1="56" y1="28" x2="500" y2="28" stroke="#E7E2D8"/>
<text x="48" y="218" text-anchor="end" font-size="11" fill="#8A94A0">0.0</text><text x="48" y="156" text-anchor="end" font-size="11" fill="#8A94A0">0.2</text><text x="48" y="94" text-anchor="end" font-size="11" fill="#8A94A0">0.4</text><text x="48" y="32" text-anchor="end" font-size="11" fill="#8A94A0">0.6</text>
<text x="76" y="238" text-anchor="middle" font-size="11" fill="#8A94A0">2</text><text x="181" y="238" text-anchor="middle" font-size="11" fill="#8A94A0">8</text><text x="286" y="238" text-anchor="middle" font-size="11" fill="#8A94A0">14</text><text x="391" y="238" text-anchor="middle" font-size="11" fill="#8A94A0">24</text><text x="496" y="238" text-anchor="middle" font-size="11" fill="#8A94A0">35</text>
<text x="278" y="256" text-anchor="middle" font-size="11.5" fill="#8A94A0">child age, months</text>
<path d="M76 62 C 120 74, 150 108, 181 122 C 220 138, 250 130, 286 132 C 340 134, 400 129, 496 131 L496 214 L76 214 Z" fill="#087BF3" opacity="0.10"/>
<path d="M76 62 C 120 74, 150 108, 181 122 C 220 138, 250 130, 286 132 C 340 134, 400 129, 496 131" fill="none" stroke="#087BF3" stroke-width="3.2" stroke-linecap="round"/>
<circle cx="76" cy="62" r="6" fill="#087BF3" stroke="#fff" stroke-width="2.5"/><circle cx="286" cy="132" r="6" fill="#087BF3" stroke="#fff" stroke-width="2.5"/>
<rect x="88" y="44" width="52" height="22" rx="11" fill="#081B46"/><text x="114" y="59.5" text-anchor="middle" font-size="12.5" font-weight="800" fill="#fff">0.49</text>
<rect x="298" y="140" width="52" height="22" rx="11" fill="#081B46"/><text x="324" y="155.5" text-anchor="middle" font-size="12.5" font-weight="800" fill="#fff">0.27</text>
<text x="496" y="118" text-anchor="end" font-size="12" font-weight="700" fill="#087BF3">more distinct, still linked</text><text x="150" y="58" font-size="12" font-weight="700" fill="#087BF3">closely linked</text><text x="14" y="130" transform="rotate(-90 14 130)" text-anchor="middle" font-size="11" fill="#8A94A0">how linked the four areas are (0 to 1)</text>
</svg><p class="cap">Kinedu record, 2020–2023 · children observed at consecutive ages between 2 and 35 months · technical name: within-child coupling</p></div>"""
# ====================================================================
# CSS extra para la versión "landing" (escaneable)
# ====================================================================
COMMON_CSS = COMMON_CSS.replace("</style>", """
.sci26-lead{max-width:720px}
.sci-take{font-size:clamp(19px,2.4vw,24px);font-weight:700;line-height:1.35;letter-spacing:-.02em;color:#081B46;text-align:center;max-width:760px;margin:28px auto 0;text-wrap:balance}
.sci-take .mk{background:linear-gradient(transparent 58%,rgba(255,189,21,.38) 58%)}
.sci-pts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:26px auto 0;max-width:1040px}
.sci-pt{background:#fff;border:1px solid #EBE6DF;border-radius:18px;padding:22px 22px 20px;text-align:left}
.sci-pt .n{display:inline-flex;width:28px;height:28px;border-radius:99px;background:var(--sciacc,#087BF3);color:#fff;font-weight:800;font-size:13px;align-items:center;justify-content:center;margin-bottom:12px}
.sci-pt b{display:block;font-size:17px;line-height:1.3;color:#081B46;margin-bottom:6px;letter-spacing:-.01em}
.sci-pt p{margin:0;font-size:14.5px;line-height:1.55;color:#52607A}
.sci-four{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:960px;margin:26px auto 0}
.sci-four a{display:flex;flex-direction:column;align-items:flex-start;text-align:left;background:var(--bg);border:1.5px solid transparent;border-radius:20px;padding:20px 18px 18px;text-decoration:none;color:#081B46;transition:transform .15s,border-color .15s,box-shadow .15s}
.sci-four a:hover{transform:translateY(-3px);border-color:var(--c);box-shadow:0 16px 34px -18px var(--c)}
.sci-four .ic{width:40px;height:40px;border-radius:99px;background:#fff;color:var(--c);display:inline-flex;align-items:center;justify-content:center;margin-bottom:14px;box-shadow:0 4px 12px rgba(8,27,70,.08)}
.sci-four .ic svg{width:22px;height:22px}
.sci-four a .k{display:block;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--c);margin-bottom:4px}
.sci-four a b{font-size:18px;line-height:1.2;margin-bottom:6px}
.sci-four a small{font-size:13.5px;line-height:1.4;color:#52607A}
.sci-line{font-size:16.5px;line-height:1.6;color:#52607A;text-align:center;max-width:720px;margin:22px auto 0;text-wrap:pretty}
.sci-line strong{color:#081B46}
.sci-rally{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin:28px auto 0;max-width:980px}
.sci-rally .st{display:flex;flex-direction:column;align-items:flex-start;padding:16px 18px 16px 16px;border-radius:18px;background:color-mix(in srgb,var(--c) 9%,#fff);border:1px solid color-mix(in srgb,var(--c) 25%,#fff);min-width:160px}
.sci-rally .av{width:36px;height:36px;border-radius:99px;background:var(--c);color:#fff;display:inline-flex;align-items:center;justify-content:center;margin-bottom:10px}
.sci-rally .av svg{width:20px;height:20px}
.sci-rally .baby{--c:#F7567C}.sci-rally .you{--c:#087BF3}
.sci-rally .who{font-size:11.5px;color:var(--c);font-weight:800;text-transform:uppercase;letter-spacing:.08em}
.sci-rally b{font-size:17px;color:#081B46;margin-top:2px}
.sci-rally .arr{font-size:22px;font-weight:800;color:#C9D2E0}
.sci-rally .more{background:transparent;box-shadow:none;border-left:0;font-size:14px;color:#52607A;font-weight:600;padding:0 4px;min-width:0}
@media(max-width:700px){.sci-rally{flex-direction:column;align-items:stretch}.sci-rally .arr{transform:rotate(90deg);text-align:center}.sci-rally .more{text-align:center}}
.sci-states .sci-state p,.sci-honest .c p{font-size:14.5px}
.sci-cancan{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:1000px;margin:26px auto 0;text-align:left}
.sci-cc{background:#fff;border:1px solid #EBE6DF;border-radius:20px;padding:22px 24px}
.sci-cc .h{display:flex;align-items:center;gap:10px;font-weight:800;font-size:16px;color:#081B46;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid #F0ECE4}
.sci-cc .i{width:26px;height:26px;border-radius:99px;display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff}
.sci-cc.can .i{background:#2EA84F}.sci-cc.cannot .i{background:#F7567C}
.sci-cc .r{font-size:15px;line-height:1.55;color:#52607A;padding:9px 0;border-bottom:1px dashed #F0ECE4}
.sci-cc .r:last-child{border-bottom:0;padding-bottom:0}
.sci-cc .r b{color:#081B46}
@media(max-width:760px){.sci-cancan{grid-template-columns:1fr}}

.sci-day{position:relative;display:flex;justify-content:space-between;align-items:flex-start;gap:8px;max-width:980px;margin:28px auto 0;padding:0 6px}
.sci-day::before{content:'';position:absolute;left:8%;right:8%;top:26px;height:3px;background:linear-gradient(90deg,#E8A33D,#913FA3);border-radius:3px;opacity:.5}
.sci-day .d{position:relative;flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;min-width:0}
.sci-day .i{width:52px;height:52px;border-radius:99px;background:#fff;border:2px solid #913FA3;color:#913FA3;display:inline-flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(8,27,70,.10);font-size:22px;font-weight:800}
.sci-day .i svg{width:24px;height:24px}
.sci-day b{display:block;font-size:14.5px;color:#081B46;margin-top:10px;line-height:1.25}
.sci-day .again .i{background:#913FA3;color:#fff}
.sci-day .again b{color:#913FA3}
@media(max-width:760px){.sci-day{flex-wrap:wrap;justify-content:center;gap:16px 10px}.sci-day::before{display:none}.sci-day .d{flex:0 0 30%}}
.sci-spec2{max-width:1040px;margin:26px auto 0}
.sci-spec2 .ends{display:flex;justify-content:space-between;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#8A94A8;margin-bottom:10px}
.sci-spec2 .track{position:relative;height:12px;border-radius:99px;background:linear-gradient(90deg,#2EA84F,#087BF3 38%,#E8A33D 66%,#913FA3)}
.sci-spec2 .track i{position:absolute;top:50%;width:22px;height:22px;border-radius:99px;border:4px solid #fff;transform:translate(-50%,-50%);box-shadow:0 4px 12px rgba(8,27,70,.18)}
.sci-spec2 .cols{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:22px;text-align:left}
.sci-spec2 .cols>div{background:#fff;border-radius:18px;padding:18px 18px 20px;border:1px solid #EBE6DF;box-shadow:0 10px 26px -18px rgba(8,27,70,.25)}
.sci-spec2 .ic{display:inline-flex;width:40px;height:40px;border-radius:12px;background:color-mix(in srgb,var(--c) 12%,#fff);color:var(--c);align-items:center;justify-content:center;margin-bottom:12px}
.sci-spec2 .ic svg{width:22px;height:22px}
.sci-spec2 .role{display:block;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--c);margin-bottom:6px}
.sci-spec2 b{display:block;font-size:18px;color:#081B46;margin-bottom:6px}
.sci-spec2 p{margin:0;font-size:14.5px;line-height:1.55;color:#52607A}
@media(max-width:760px){.sci-spec2 .cols{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.sci-spec2 .cols{grid-template-columns:1fr}}
.sci-two-stat{grid-template-columns:1fr 1.6fr;align-items:stretch}
.sci-two-stat>*{height:100%;box-sizing:border-box}
.sci-stat{background:#fff;border:1px solid #EBE6DF;border-radius:20px;padding:28px 26px;display:flex;flex-direction:column;justify-content:center;text-align:left}
.sci-stat .n{font-size:clamp(56px,7vw,84px);font-weight:800;letter-spacing:-.04em;line-height:1;color:#913FA3;margin-bottom:12px}
.sci-stat p{margin:0;font-size:16.5px;line-height:1.5;color:#33415C;text-wrap:pretty}
.sci-stat .rest{margin-top:12px;font-weight:800;color:#081B46}
@media(max-width:760px){.sci-two-stat{grid-template-columns:1fr}}
.sci-docs{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.sci-doc{display:inline-flex;align-items:center;gap:12px;padding:12px 18px 12px 14px;border-radius:14px;border:1px dashed #C9D2E0;background:transparent;color:#33415C;text-decoration:none;transition:border-color .15s,background .15s}
.sci-doc:hover{border-color:#087BF3;background:#fff;color:#087BF3}
.sci-doc svg{flex-shrink:0;color:#8A94A8}
.sci-doc:hover svg{color:#087BF3}
.sci-doc span{display:flex;flex-direction:column;text-align:left;font-weight:700;font-size:14.5px;line-height:1.2}
.sci-doc small{font-weight:500;font-size:12px;color:#8A94A8;margin-top:3px}
.sci-two{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:1060px;margin:30px auto 0;align-items:start}
.sci-two .sci26-chart{max-width:none;margin:0}
.sci-fadebars{max-width:820px;margin:26px auto 0;background:#fff;border:1px solid #EBE6DF;border-radius:20px;padding:22px 24px 26px;text-align:left}
.sci-fadebars .h{font-size:16px;font-weight:800;color:#081B46;margin-bottom:18px}
.sci-fadebars .row{display:grid;grid-template-columns:190px 1fr;gap:16px;align-items:center;margin-top:16px}
.sci-fadebars .lbl{font-size:14.5px;font-weight:700;color:#081B46}
.sci-fadebars .track{position:relative;height:16px;border-radius:99px;background:#F1EFE9;padding-bottom:22px;box-sizing:content-box}
.sci-fadebars .bar{position:absolute;left:0;top:0;height:16px;border-radius:99px}
.sci-fadebars .bar.long{width:100%;background:linear-gradient(90deg,#913FA3 0%,rgba(145,63,163,.55) 25%,rgba(145,63,163,.08) 100%)}
.sci-fadebars .bar.short{width:24%;background:linear-gradient(90deg,#913FA3,rgba(145,63,163,.7))}
.sci-fadebars span{position:absolute;top:22px;font-size:12px;color:#52607A;white-space:nowrap}
.sci-fadebars .m1{left:0}.sci-fadebars .m2{right:0}
@media(max-width:760px){.sci-two{grid-template-columns:1fr}.sci-fadebars .row{grid-template-columns:1fr;gap:8px}.sci-fadebars span{white-space:normal;max-width:48%}}
.sci-path{position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;max-width:980px;margin:30px auto 0}
.sci-path::before{content:'';position:absolute;left:12%;right:12%;top:41px;height:3px;background:linear-gradient(90deg,#E4DED4,#087BF3);border-radius:3px}
.sci-path .st{position:relative;text-align:center;padding-top:0}
.sci-path .k{display:block;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8A94A8;height:22px;margin-bottom:8px}
.sci-path .dot{display:block;width:18px;height:18px;border-radius:99px;background:#fff;border:3px solid #C9D2E0;margin:0 auto 14px;position:relative;z-index:1}
.sci-path .last .dot{width:24px;height:24px;border-color:#087BF3;background:#087BF3;box-shadow:0 0 0 6px rgba(8,123,243,.15);margin-top:-3px;margin-bottom:11px}
.sci-path b{display:block;font-size:16px;color:#081B46;line-height:1.3;max-width:200px;margin:0 auto}
.sci-path .last b{color:#087BF3}
.sci-spec{max-width:980px;margin:26px auto 0}
.sci-spec .bar{display:flex;height:14px;border-radius:99px;overflow:hidden;gap:3px}
.sci-spec .bar i{flex:1;display:block}
.sci-spec .legend{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:16px;text-align:left}
.sci-spec .legend img{display:block;width:32px;height:32px;margin-bottom:8px}
.sci-spec .legend b{display:block;font-size:16px;margin-bottom:4px}
.sci-spec .legend p{margin:0;font-size:14px;line-height:1.5;color:#52607A}
@media(max-width:760px){.sci-path{grid-template-columns:1fr 1fr;gap:22px 12px}.sci-path::before{display:none}.sci-spec .legend{grid-template-columns:1fr 1fr}}
.sci-bridge{display:grid;grid-template-columns:1fr 44px 1fr;gap:16px;align-items:stretch;max-width:1000px;margin:26px auto 0;text-align:left}
.sci-then,.sci-now{background:#fff;border:1px solid #EBE6DF;border-radius:22px;padding:24px;display:flex;flex-direction:column;justify-content:center}
.sci-now{border:2px solid #087BF3;box-shadow:0 18px 44px rgba(8,123,243,.12)}
.sci-then .k,.sci-now .k{font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8A94A8;margin-bottom:14px}
.sci-now .k{color:#087BF3}
.sci-then p{margin:16px 0 0;font-size:15px;line-height:1.55;color:#52607A}
.sci-now .q{font-size:clamp(20px,2.4vw,25px);font-weight:800;line-height:1.25;letter-spacing:-.02em;color:#081B46;margin:0 0 18px;text-wrap:balance}
.sci-now .q .pre{display:block;font-weight:500;font-size:15.5px;color:#52607A;margin-bottom:8px;letter-spacing:0}
.sci-now .a{margin:18px 0 0;font-size:15.5px;line-height:1.55;color:#33415C}
.sci-now .a strong{display:block;color:#081B46;font-size:19px;line-height:1.3;margin-bottom:8px}
.sci-arrow{display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:800;color:#C9D2E0}
.sci-areas4{display:flex;justify-content:center;padding:6px 0}
.sci-areas4 span{width:64px;height:64px;border-radius:99px;background:#fff;border:3px solid var(--c);display:inline-flex;align-items:center;justify-content:center;margin-left:-12px;box-shadow:0 6px 18px rgba(8,27,70,.10)}
.sci-areas4 span:first-child{margin-left:0}
.sci-areas4 img{width:36px;height:36px}
.sci26-acts{align-items:end!important}
.sci26-act:nth-child(1) .big{font-size:30px!important}
.sci26-act:nth-child(2) .big{font-size:46px!important}
.sci26-act:nth-child(3) .big{font-size:64px!important;color:var(--sciacc)!important}
@media(min-width:781px){.sci26-act:nth-child(1){min-height:290px}.sci26-act:nth-child(2){min-height:365px}.sci26-act:nth-child(3){min-height:440px;border:2px solid var(--sciacc);box-shadow:0 18px 44px rgba(247,86,124,.16)}}
.sci26-act{position:relative}
.sci26-act:nth-child(n+2)::after{content:'→';position:absolute;left:-24px;top:42%;font-size:22px;font-weight:800;color:#C9D2E0}
@media(max-width:780px){.sci26-act:nth-child(n+2)::after{content:'↓';left:50%;top:-24px;transform:translateX(-50%)}.sci-bridge{grid-template-columns:1fr}.sci-arrow{transform:rotate(90deg);height:34px}}
@media(max-width:900px){.sci-pts{grid-template-columns:1fr}.sci-four{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.sci-four{grid-template-columns:1fr 1fr}.sci-four a{font-size:14px;padding:14px 12px}}
</style>""")

MOBILE_CSS = """@media(max-width:640px){
.sci-chapters-in{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:12px 16px;gap:8px;scrollbar-width:none}
.sci-chapters-in::-webkit-scrollbar{display:none}
.sci-chapters .lbl{display:none}
.sci-chapters a{flex:0 0 auto;white-space:nowrap}
.sci26-kick{justify-content:center;text-align:center;font-size:11px;letter-spacing:.08em;padding:7px 14px}
.sci-squig::after{bottom:-1px;height:7px}
.sci26 h2{line-height:1.22}
.sci-day .again{flex:0 0 100%;flex-direction:row;justify-content:center;gap:10px;margin-top:6px}
.sci-day .again b{margin-top:0}
.sci-day .again .i{width:40px;height:40px;font-size:18px}
.sci-spec2 .track,.sci-spec2 .ends{display:none}
.sci-app{padding:18px 16px}
.sci-app .draft{right:12px}
.sci-btn{padding:14px 22px;font-size:15px}
.sci-btn-xl{padding:18px 28px;font-size:16.5px}
.sci26-acts .sci26-act{min-height:0!important}
}"""
COMMON_CSS = COMMON_CSS.replace("</style>", MOBILE_CSS+"\n</style>")

def pts(items):
    return '<div class="sci-pts">'+"".join('<div class="sci-pt"><span class="n">%d</span><b>%s</b><p>%s</p></div>'%(i+1,b,p) for i,(b,p) in enumerate(items))+'</div>'
def take(html): return '<p class="sci-take">%s</p>'%html
def line(html): return '<p class="sci-line">%s</p>'%html
def ctas_assess(): return '<p style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px">'+cta("Take the free assessment", ASSESS)+cta("Start free", TRY, False)+'</p>'

HONEST1=[("Kinedu does not diagnose.","It shows you what is worth raising with your pediatrician. Only your doctor can tell you if something is wrong."),
 ("Our data knows what children did.","Not what their parents did. Nothing in it is a verdict on you."),
 ("These are families who chose an app.","They describe this population well. How well they describe everyone else, we only partly know.")]

# ====================================================================
# PÁGINA 1 · How we got here
# ====================================================================
p1_hero = hero("The science behind Kinedu · Part 1 of 3",
    'Kinedu is built on how <span class="gradient-shift">3.5 million</span> babies actually grew.',
    "Studied with Stanford and turned into an assessment that shows what your baby is ready for next. This is the science behind it.",
    "")

CHECKLIST_SVG = """<svg viewBox="0 0 320 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="An old-style milestone checklist by age" style="width:100%;max-width:320px;height:auto;display:block;margin:0 auto">
<rect x="10" y="8" width="300" height="234" rx="14" fill="#fff" stroke="#E4DED4"/>
<rect x="10" y="8" width="300" height="46" rx="14" fill="#F3F0EA"/><rect x="10" y="40" width="300" height="14" fill="#F3F0EA"/>
<text x="30" y="37" font-size="14" font-weight="800" fill="#52607A" font-family="Proxima Nova,Arial,sans-serif">By 9 months</text>
<g font-size="13.5" fill="#33415C" font-family="Proxima Nova,Arial,sans-serif">
<rect x="30" y="72" width="18" height="18" rx="4" fill="#2EA84F"/><path d="M34 81 l4 4 l7 -8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><text x="60" y="86">Sits without support</text>
<rect x="30" y="110" width="18" height="18" rx="4" fill="#2EA84F"/><path d="M34 119 l4 4 l7 -8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><text x="60" y="124">Passes a toy from hand to hand</text>
<rect x="30" y="148" width="18" height="18" rx="4" fill="#fff" stroke="#C9D2E0" stroke-width="1.5"/><text x="60" y="162">Says “mama” or “dada”</text>
<rect x="30" y="186" width="18" height="18" rx="4" fill="#fff" stroke="#C9D2E0" stroke-width="1.5"/><text x="60" y="200">Pulls up to stand</text>
</g>
<text x="30" y="230" font-size="11.5" fill="#8A94A8" font-family="Proxima Nova,Arial,sans-serif">yes / no · by age · one line per milestone</text>
</svg>"""

AREAS4 = '<div class="sci-areas4">' + "".join('<span style="--c:%s"><img src="/images/areas/%s.png" alt="" width="40" height="40" loading="lazy"></span>'%(c,f) for c,f in (("#1E88E5","physical"),("#2EA84F","cognitive"),("#E8A33D","linguistic"),("#D6497B","emotional"))) + '</div>'

p1_bridge = sec("From milestones to a clearer picture", 'How Kinedu’s assessment <span class="sci-squig">has evolved.</span>', "",
 '<div class="sci-bridge">'
 '<div class="sci-then"><div class="k">2013 · Where Kinedu started</div>'+CHECKLIST_SVG+'<p>Kinedu began with an age-based milestone checklist: one item at a time, with a yes-or-no answer. It was a simple way to record what a baby could already do. We wanted to show more of how those skills develop.</p></div>'
 '<div class="sci-arrow" aria-hidden="true">→</div>'
 '<div class="sci-now"><div class="k">Today · Where Kinedu is</div><p class="q">How do the four areas of development connect?</p>'+AREAS4+'<p class="a"><strong>Closely linked early on. More distinct as children grow.</strong> We used that insight to look at skills together and build a fuller picture of development.</p></div>'
 '</div>'+line("Here are three key steps in that journey."), "#2EA84F", "", 1060)

p1_acts = sec("How we got there", 'Built by Kinedu. Studied by <span class="sci-squig">Stanford researchers.</span> Informed by millions of children.',
 "From the first assessment to research at a much larger scale.",
 """<div class="sci26-acts">
<div class="sci26-act"><span class="n">1</span><div class="big">2,135</div><div class="unit">caregivers</div><p>We tested the first assessment with 2,135 caregivers to check how well the questions worked. Stanford researcher Michael C. Frank helped review the milestones for children from birth to 24 months.</p></div>
<div class="sci26-act"><span class="n">2</span><div class="big">21,861</div><div class="unit">children</div><p>Researchers Stenhaug, Ram, and Frank analyzed Kinedu data from 21,861 children. They found that the four areas of development were more closely linked early in life and became more distinct with age. They shared the results in the preprint “The Structure of Developmental Variation in Early Childhood”.</p></div>
<div class="sci26-act"><span class="n">3</span><div class="big">3.5M</div><div class="unit">children</div><p>We expanded the analysis using 281 million validated caregiver observations from 3.5 million children. The broader pattern held: developmental areas were more closely linked early on and became more distinct with age. Our expected ages also lined up with the data, with a median difference of zero months.</p></div>
</div>
<p class="sci-quote" style="margin-top:34px">That research helped us map <span class="mk">how skills develop and connect.</span></p>""", "#F7567C")

p1_rebuilt = sec("The rebuild", 'We rebuilt the assessment around <span class="sci-squig">a different question.</span>',
 "We wanted to understand how a skill is taking shape.<br>Walking begins well before those first independent steps:",
 """<div class="sci-path">
<div class="st"><span class="k">months earlier</span><span class="dot"></span><b>Pulls up to stand</b></div>
<div class="st"><span class="k">then</span><span class="dot"></span><b>Walks while holding onto the sofa</b></div>
<div class="st"><span class="k">then</span><span class="dot"></span><b>Takes steps while holding your hand</b></div>
<div class="st last"><span class="k">and finally</span><span class="dot"></span><b>Takes steps independently</b></div>
</div>
"""+line("Every skill in Kinedu is shown along a path like this one:")+"""
<div class="sci-spec" style="position:relative">
<div class="bar"><i style="background:#913FA3"></i><i style="background:#1248B7"></i><i style="background:#3EB646"></i><i style="background:#EEBD0E"></i></div>
<div class="legend">
<div><img src="/images/states/upcoming.png" alt="" width="32" height="32" loading="lazy"><b style="color:#913FA3">Upcoming</b><p>Skills that usually appear later than your baby’s current age.</p></div>
<div><img src="/images/states/reinforce.png" alt="" width="32" height="32" loading="lazy"><b style="color:#1248B7">Reinforce</b><p>Skills expected around this age that your baby is still working on.</p></div>
<div><img src="/images/states/ontrack.png" alt="" width="32" height="32" loading="lazy"><b style="color:#3EB646">On track</b><p>Skills your baby is showing at the expected age.</p></div>
<div><img src="/images/states/mastered.png" alt="" width="32" height="32" loading="lazy"><b style="color:#D9A800">Mastered</b><p>Skills your baby already shows consistently.</p></div>
</div>
</div>
<p class="sci-quote">A clearer picture of the skills your baby is building <span class="mk">and what may come next.</span></p>""", "#087BF3", "sci26-mint")

p1_product = '<section id="assessment" class="sci26" style="--sciacc:#2EA84F"><div class="sci26-wrap" style="max-width:860px"><div class="sci26-kick">How the assessment works</div><h2>Answer simple questions about what your baby does. <span class="sci-squig">That’s it.</span></h2><p class="sci26-lead">You can answer at home, based on what you see every day. Here’s a sample question from the assessment for 12&#8209;month&#8209;olds:</p>\n' + SCIQ + '</div></section>'

p1_instrument = sec("Why we ask what we ask", 'Questions chosen to capture <span class="sci-squig">developing skills.</span>',
 "A “not yet” answer doesn’t tell the whole story. We look at it alongside your baby’s age and other answers to understand how their skills are developing.",
 '<div class="sci26-edge"><div class="sci-prose"><p class="big" style="font-size:clamp(19px,2.3vw,24px)">Your answers help us build a picture.</p><p>We compare your answers with patterns in caregiver reports across ages. Together, they help us understand which skills your baby is developing. You don’t need special training to answer.</p></div>'+CH_HEAD+'</div>', "#1FA66E")

p1_areas = sec("What the assessment covers", '414 milestones. 46 skills. <span class="sci-squig">Four areas.</span>',
 "The assessment covers physical, cognitive, language, and social-emotional development. These areas are closely connected early in life and become more distinct as children grow.",
 """<div class="sci26-areas">
<div class="sci26-area" style="background:#E3F0FE"><img class="ic" src="/images/areas/physical.png" alt="" width="44" height="44" loading="lazy"><div class="t">Physical</div><div class="c" style="color:#1E88E5">From holding their head up to jumping on one foot.</div><p>How your child moves and uses their body.</p></div>
<div class="sci26-area" style="background:#E4F6E7"><img class="ic" src="/images/areas/cognitive.png" alt="" width="44" height="44" loading="lazy"><div class="t">Cognitive</div><div class="c" style="color:#2EA84F">Exploring, solving problems, and playing pretend.</div><p>How your child learns about the world.</p></div>
<div class="sci26-area" style="background:#FDEBD8"><img class="ic" src="/images/areas/linguistic.png" alt="" width="44" height="44" loading="lazy"><div class="t">Language</div><div class="c" style="color:#E8A33D">From babbling to words and sentences.</div><p>How your child understands and communicates.</p></div>
<div class="sci26-area" style="background:#FBE3ED"><img class="ic" src="/images/areas/emotional.png" alt="" width="44" height="44" loading="lazy"><div class="t">Social-emotional</div><div class="c" style="color:#D6497B">Connecting, expressing feelings, and playing with others.</div><p>How your child relates to people and handles emotions.</p></div>
</div>""", "#0E3687", "sci26-blue")

p1_honest = honest(tail=READ_WORK)

p1_cta = sec("Your turn", 'See which skills your baby <span class="pg-squig">is building.</span>',
 "In about five minutes, answer questions about everyday behaviors and get a clearer picture of your baby’s developing skills.",
 ctas_assess()+'<p style="font-family:\'DM Mono\',monospace;font-size:11.5px;color:#8A94A8;margin-top:18px;text-align:center">Developmental surveillance. Not a diagnosis.</p>', "#F7567C", "sci26-mint", 840)

page1 = page("/science", "The Science Behind Kinedu: How We Got Here | Kinedu",
 "We watched 3.5 million children grow up. What we learned made us rebuild Kinedu: from a milestone checklist to an assessment that shows what is emerging.",
 "/science", p1_hero, [p1_bridge, p1_acts, p1_rebuilt, p1_product, p1_instrument, p1_areas, p1_honest, p1_cta, p3_note, nextprev(None, ("/science-what-we-know","How babies grow"))],
 og_title="Kinedu is built on how 3.5 million babies actually grew | Kinedu")

# ====================================================================
# PÁGINA 2 · Five things we know
# ====================================================================
COUPLING_SVG = COUPLING_SVG.replace('<p style="font-size:14.5px;color:#52607A;line-height:1.6;margin:0 0 16px">Following the same children from 2 to 35 months.</p>',
                                    '<p style="font-size:14.5px;color:#52607A;line-height:1.6;margin:0 0 16px">This measure shows how closely progress across the four areas is linked. It falls by almost half during the first year, then remains more stable through the ages shown.</p>')

p2_hero = hero("The science behind Kinedu · Part 2 of 3",
    'Five things we know about <span class="gradient-shift">how babies grow.</span>',
    "What 3.5 million children taught us about the first three years.",
    "")

p2_intro = sec("Why five", 'Five patterns that help <span class="sci-squig">explain development.</span>',
 "Together, these ideas help make sense of how skills connect, when they appear, and why children develop at different paces.", "", "#087BF3", "", 860, "padding-top:60px;padding-bottom:30px")

def proof(text): return '<div class="sci-proof"><span class="tag">Proof</span><p>%s</p></div>'%text

p2_one = sec("One · Together", 'Early skills <span class="sci-squig">develop together.</span>',
 "Holding their head up gives your baby new ways to look around and interact. It’s one example of how movement, learning, communication, and relationships connect.",
 CH_FAN + '<div style="margin-top:30px">' + COUPLING_SVG + '</div>', "#2EA84F", "sci26-mint", 1060)

p2_two = sec("Two · In order", 'Skills build on <span class="sci-squig">earlier skills.</span>',
 "Babbling helps lay the groundwork for words. Pulling up to stand helps prepare the way for independent steps. These sequences help us understand what a child may be working toward.",
 SEQ + '<p class="sci26-note" style="margin-top:14px">Expected age: when three in four children have the skill · The order is typical, the timing varies · Kinedu record</p>\n<div class="sci-two">' + CH_BABBLE + CH_WALK + '</div>', "#E8A33D", "", 1060)

p2_three = sec("Three · Wide", 'Children reach milestones across a wide <span class="sci-squig">range of ages.</span>',
 "For some skills, children reach them within a few months of one another. For others, the range spans well over a year, and it tends to widen as children grow.",
 DISP+'<p class="sci-quote" style="font-size:clamp(21px,3vw,30px)">An expected age is <span class="mk">a reference point, not a deadline.</span></p>', "#F7567C", "sci26-blue", 1060)

p2_four = sec("Four · Windows", 'A learning window <span class="sci-squig">isn’t a countdown.</span>',
 "The chart shows when reports of these skills become more common in our data. These age ranges describe a pattern, not a deadline for an individual child.",
 WIN, "#087BF3", "", 1060)

p2_five = sec("Five · Unpredictable", 'Today’s assessment doesn’t tell your child’s <span class="sci-squig">whole future.</span>',
 "A child’s current skill level tells us little about how quickly they’ll progress next. Where they are today and their pace of development are different things.",
 """<div class="sci26-chart" style="max-width:1000px;margin:26px auto 0"><h3 style="font-size:20px;font-weight:800;color:#081B46;margin:0 0 8px">An assessment is a photograph, not a prophecy.</h3>
<p style="font-size:14.5px;color:#52607A;line-height:1.6;margin:0 0 12px">Each assessment captures a moment in your child’s development. Checking in again helps you see what has changed.</p>
<div class="pg-vdesk"><svg viewBox="0 0 940 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="An assessment is a photograph: one taken at 3 months says little by age 2, one taken at 2 years still says a lot three months later, so check in again every few months" font-family="Proxima Nova,Arial,sans-serif"><line x1="70" y1="150" x2="930" y2="150" stroke="#E7E2D8" stroke-width="2"/><circle cx="70" cy="150" r="3" fill="#D9D2C7"/><text x="70" y="172" text-anchor="middle" font-size="11.5" fill="#8A94A0">0</text><circle cx="213" cy="150" r="3" fill="#D9D2C7"/><text x="213" y="172" text-anchor="middle" font-size="11.5" fill="#8A94A0">6</text><circle cx="356" cy="150" r="3" fill="#D9D2C7"/><text x="356" y="172" text-anchor="middle" font-size="11.5" fill="#8A94A0">12</text><circle cx="500" cy="150" r="3" fill="#D9D2C7"/><text x="500" y="172" text-anchor="middle" font-size="11.5" fill="#8A94A0">18</text><circle cx="643" cy="150" r="3" fill="#D9D2C7"/><text x="643" y="172" text-anchor="middle" font-size="11.5" fill="#8A94A0">24</text><circle cx="786" cy="150" r="3" fill="#D9D2C7"/><text x="786" y="172" text-anchor="middle" font-size="11.5" fill="#8A94A0">30</text><circle cx="930" cy="150" r="3" fill="#D9D2C7"/><text x="930" y="172" text-anchor="middle" font-size="11.5" fill="#8A94A0">36</text><text x="500" y="192" text-anchor="middle" font-size="12" fill="#8A94A0">your baby’s age, months</text><defs><linearGradient id="fade1" x1="0" x2="1"><stop offset="0" stop-color="#913FA3" stop-opacity=".9"/><stop offset="1" stop-color="#913FA3" stop-opacity="0"/></linearGradient></defs><rect x="141" y="96" width="573" height="14" rx="7" fill="url(#fade1)"/><g transform="translate(141,86)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#913FA3"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#913FA3"/></g><text x="128" y="66" font-size="12.5" font-weight="800" fill="#913FA3">Assessment at 3 months</text><text x="142" y="128" font-size="11.5" fill="#52607A">at age 2, it says little about where they stand</text><rect x="643" y="96" width="72" height="14" rx="7" fill="#087BF3" opacity=".9"/><g transform="translate(643,86)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#087BF3"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#087BF3"/></g><text x="630" y="66" font-size="12.5" font-weight="800" fill="#087BF3">Assessment at 2 years</text><text x="930" y="128" text-anchor="end" font-size="11.5" fill="#52607A">3 months later, it still says a lot about where they stand</text><text x="70" y="232" font-size="13" font-weight="800" fill="#081B46">Checking in again:</text><text x="200" y="232" font-size="12.5" fill="#52607A">a new picture every few months</text><line x1="141" y1="268" x2="858" y2="268" stroke="#C9D2E0" stroke-width="2" stroke-dasharray="4 6"/><g transform="translate(141,268)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#1FA66E"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#1FA66E"/></g><g transform="translate(285,268)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#8FD6B5"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#8FD6B5"/></g><g transform="translate(428,268)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#8FD6B5"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#8FD6B5"/></g><g transform="translate(571,268)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#8FD6B5"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#8FD6B5"/></g><g transform="translate(715,268)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#8FD6B5"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#8FD6B5"/></g><g transform="translate(858,268)"><rect x="-13" y="-9" width="26" height="20" rx="5" fill="#8FD6B5"/><circle cx="0" cy="1.5" r="5" fill="#fff"/><rect x="-5" y="-13" width="10" height="5" rx="2" fill="#8FD6B5"/></g></svg></div><div class="pg-vmob" style="max-width:none"><svg viewBox="0 0 390 330" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true" font-family="Proxima Nova,Arial,sans-serif" style="width:100%;height:auto;display:block"><defs><linearGradient id="fade1m" x1="0" x2="1"><stop offset="0" stop-color="#913FA3" stop-opacity=".9"/><stop offset="1" stop-color="#913FA3" stop-opacity="0"/></linearGradient></defs><text x="24" y="22" font-size="12.5" font-weight="800" fill="#913FA3">Assessment at 3 months</text><rect x="52" y="44" width="228" height="12" rx="6" fill="url(#fade1m)"/><g transform="translate(52,36)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#913FA3"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#913FA3"/></g><text x="280" y="76" text-anchor="end" font-size="11.5" fill="#52607A">at age 2, it says little about where they stand</text><text x="24" y="112" font-size="12.5" font-weight="800" fill="#087BF3">Assessment at 2 years</text><rect x="252" y="134" width="28" height="12" rx="6" fill="#087BF3" opacity=".9"/><g transform="translate(252,126)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#087BF3"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#087BF3"/></g><text x="366" y="166" text-anchor="end" font-size="11.5" fill="#52607A">3 months later, it still says a lot about where they stand</text><line x1="24" y1="190" x2="366" y2="190" stroke="#E7E2D8" stroke-width="2"/><circle cx="24" cy="190" r="3" fill="#D9D2C7"/><text x="24" y="210" text-anchor="middle" font-size="11" fill="#8A94A0">0</text><circle cx="138" cy="190" r="3" fill="#D9D2C7"/><text x="138" y="210" text-anchor="middle" font-size="11" fill="#8A94A0">12</text><circle cx="252" cy="190" r="3" fill="#D9D2C7"/><text x="252" y="210" text-anchor="middle" font-size="11" fill="#8A94A0">24</text><circle cx="366" cy="190" r="3" fill="#D9D2C7"/><text x="366" y="210" text-anchor="middle" font-size="11" fill="#8A94A0">36</text><text x="195" y="228" text-anchor="middle" font-size="11.5" fill="#8A94A0">your baby’s age, months</text><text x="24" y="268" font-size="12.5" font-weight="800" fill="#081B46">Checking in again:</text><text x="24" y="286" font-size="11.5" fill="#52607A">a new picture every few months</text><line x1="52" y1="314" x2="337" y2="314" stroke="#C9D2E0" stroke-width="2" stroke-dasharray="4 6"/><g transform="translate(52,314)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#1FA66E"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#1FA66E"/></g><g transform="translate(109,314)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#8FD6B5"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#8FD6B5"/></g><g transform="translate(166,314)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#8FD6B5"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#8FD6B5"/></g><g transform="translate(223,314)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#8FD6B5"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#8FD6B5"/></g><g transform="translate(280,314)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#8FD6B5"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#8FD6B5"/></g><g transform="translate(337,314)"><rect x="-11" y="-8" width="22" height="17" rx="4" fill="#8FD6B5"/><circle cx="0" cy="1" r="4" fill="#fff"/><rect x="-4" y="-11" width="8" height="4" rx="1.5" fill="#8FD6B5"/></g></svg></div></div>
"""+"<p class=\"sci26-note\" style=\"margin-top:18px\">In this analysis, current skill level explained about 1.5% of the variation in subsequent developmental pace.</p>", "#913FA3", "sci26-mint", 1060)

p2_closer = '<section class="sci26 sci26-plain" style="padding:40px 20px 56px"><div class="sci26-wrap" style="max-width:900px;text-align:center"><a href="'+ASSESS+'" class="sci-btn sci-btn-primary sci-btn-xl">See where your baby is today <span class="arr" aria-hidden="true">→</span></a><p class="sci-btn-note">About five minutes. Free, no app needed.</p></div></section>'

p2_honest = honest(cannot=CANNOT[:2]+[("Read the room for you.","About 11% of a reading is how the caregiver answers, not the child. We correct for it, and we would rather tell you than not.")])

page2 = page("/science-what-we-know", "Five Things We Know About How Babies Grow | Kinedu",
 "What 3.5 million children taught us: everything grows together, skills build in order, normal is wide, and no chart can predict your child.",
 "/science-what-we-know", p2_hero, [p2_intro, p2_one, p2_two, p2_three, p2_four, p2_five, p2_closer, p3_note, nextprev(("/science","How Kinedu was built"), ("/science-what-you-can-do","What you can do as a parent"))],
 og_title="Five things we know about how babies grow | Kinedu")

# ====================================================================
# PÁGINA 3 · So what can you do?
# ====================================================================
def app_slot(title, text, href, link):
    return ('<a class="sci-app" href="%s"><img src="/images/app/icon.png" alt="" width="52" height="52">'
            '<span class="body"><span class="k">In the Kinedu app</span><b>%s</b><p>%s</p></span><span class="go">%s <span aria-hidden="true">→</span></span></a>')%(href,title,text,link)

p3_hero = hero("The science behind Kinedu · Part 3 of 3",
    'So what can <span class="gradient-shift">you</span> do, as a parent?',
    "Four things that are actually in your hands.",
    "", badges=False)

ICO={"play":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18M3 12h18"/><path d="M12 3c-3 3-3 15 0 18M12 3c3 3 3 15 0 18"/></svg>',
     "heart":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>',
     "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
     "clock":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'}
FOUR=[("#play","One","Play","Follow their curiosity. Join the back-and-forth.","play","#2EA84F","#E4F6E7"),
      ("#relationships","Two","Relationships","Warmth, connection, and clear limits.","heart","#F7567C","#FBE3ED"),
      ("#stress","Three","Stress","Help them through difficult moments.","shield","#E8A33D","#FDEBD8"),
      ("#predictability","Four","Predictability","Build routines they can recognize.","clock","#913FA3","#F1E7F3")]
p3_open = sec("Where this comes from", 'Everyday moments give you <span class="sci-squig">ways to help.</span>',
 "Kinedu’s data help us understand how children’s skills develop. The ideas on this page come from broader research on parenting and child development. They focus on four parts of everyday life:",
 '<div class="sci-four">'+"".join('<a href="%s" style="--c:%s;--bg:%s"><span class="ic">%s</span><span class="k">%s</span><b>%s</b><small>%s</small></a>'%(h,c,bg,ICO[ic],k,t,sub) for h,k,t,sub,ic,c,bg in FOUR)+'</div>', "#087BF3", "", 960, "padding-top:60px")

p3_play = sec("One · Play", 'Play starts with the back-and-forth <span class="sci-squig">between you.</span>',
 "Your baby makes a sound. You respond. They respond again. Researchers call these back-and-forth exchanges “serve and return.” Your face, voice, and attention are part of the interaction.",
 """<div class="sci-rally">
<div class="st baby"><span class="who">Your baby</span><b>coos</b></div><span class="arr">→</span>
<div class="st you"><span class="who">You</span><b>smile or talk back</b></div><span class="arr">→</span>
<div class="st baby"><span class="who">Your baby</span><b>responds</b></div><span class="arr">↻</span>
<div class="st more">…and so on, back and forth</div>
</div>
"""+line("As your child grows, your role in play changes. Sometimes they lead. Sometimes you offer a prompt, introduce a rule, or show them how something works.")+"""
<div class="sci-spec2">
<div class="ends"><span>Your baby in charge</span><span>You in charge</span></div>
<div class="track"><i style="left:12.5%;background:#2EA84F"></i><i style="left:37.5%;background:#087BF3"></i><i style="left:62.5%;background:#E8A33D"></i><i style="left:87.5%;background:#913FA3"></i></div>
<div class="cols">
<div style="--c:#2EA84F"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="12" width="8" height="8" rx="1.5"/><rect x="13" y="12" width="8" height="8" rx="1.5"/><rect x="8" y="3" width="8" height="8" rx="1.5"/></svg></span><span class="role">Your baby leads</span><b>Free play</b><p>Your child chooses what to explore and how to use it. There’s room to invent, experiment, and follow their curiosity.</p></div>
<div style="--c:#087BF3"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h5l-1 11H4zM9.5 8h5l-1 11h-3zM16 8h5l-1 11h-3z"/></svg></span><span class="role">You set it up, they run it</span><b>Guided play</b><p>You create an opportunity or offer a prompt, while your child leads the exploration. With colored cups, for example, you might invite them to sort or compare.</p></div>
<div style="--c:#E8A33D"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8" cy="8" r="1.3" fill="currentColor"/><circle cx="16" cy="8" r="1.3" fill="currentColor"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/><circle cx="8" cy="16" r="1.3" fill="currentColor"/><circle cx="16" cy="16" r="1.3" fill="currentColor"/></svg></span><span class="role">Rules, with room to play</span><b>Games</b><p>Simple games give children practice taking turns, following rules, and trying again.</p></div>
<div style="--c:#913FA3"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M6 20V9a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v11M9 7V5a3 3 0 0 1 6 0v2M9 12h6M9 16h6"/></svg></span><span class="role">You lead</span><b>Direct instruction</b><p>You show your child how to do a specific task, then give them a chance to try.</p></div>
</div>
</div>
"""+take("Choose the approach that fits <span class=\"mk\">what your child is exploring.</span>")
 +app_slot("Daily activity ideas", "Short videos that show you how to try activities with your baby.", TRY, "Try it free"), "#2EA84F", "sci26-mint", 1040)
p3_play = p3_play.replace('<section class="sci26', '<section id="play" class="sci26', 1)

p3_rel = sec("Two · Relationships", 'Warmth and clear limits <span class="sci-squig">can go together.</span>',
 "You can respond to your child’s feelings while keeping a clear limit. The goal is to offer support and expectations that fit their age.",
 pts([("You can say no with care.","Your child can feel upset about a limit and still receive your comfort and support."),
      ("Keep the limit. Stay connected.","Acknowledge the feeling and explain the boundary in simple words."),
      ("Help them find their calm.","Offer a calm voice and support while they learn to handle strong feelings.")])
 +line("You won’t get every moment right. You can reconnect and try again.")
 +app_slot("Live classes and the Positive Education masterclass", "Learn ways to set limits with care and respond to tantrums, with guidance from child psychologists.", "/live-classes", "See live classes"), "#F7567C", "", 1040)
p3_rel = p3_rel.replace('<section class="sci26', '<section id="relationships" class="sci26', 1)

p3_stress = sec("Three · Stress", 'Not all stress is <span class="sci-squig">the same.</span>',
 "Harvard’s Center on the Developing Child describes three types of stress response: positive, tolerable, and toxic. The intensity, duration, and support available to a child matter.",
 """<div class="sci-stress">
<div class="c" style="background:#E4F6E7"><b>Positive</b><p>A brief challenge, with support from a caring adult, followed by a return to calm.</p></div>
<div class="c" style="background:#FDEBD8"><b>Tolerable</b><p>A more serious difficulty. Supportive relationships help the child cope and recover.</p></div>
<div class="c" style="background:#FBE3ED"><b>Toxic</b><p>Prolonged or excessive stress without adequate adult support. This can affect development and long-term health.</p></div>
</div>
"""+take("Your support can help your child <span class=\"mk\">through difficult moments.</span>")
 +app_slot("Ask an expert live", "Bring your questions to a live class.", "/live-classes", "See live classes"), "#E8A33D", "sci26-blue", 1040)
p3_stress = p3_stress.replace('<section class="sci26', '<section id="stress" class="sci26', 1)

DAY=[("wake","Wake up"),("meal","Meals"),("play","Play"),("nap","Nap"),("bath","Bath"),("bed","Bedtime")]
DAY_ICO={"wake":'<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
 "meal":'<path d="M4 3v7a3 3 0 0 0 3 3v8M7 3v7M10 3v7M17 3c-2 0-3 3-3 7h3v11"/>',
 "play":'<rect x="3" y="11" width="8" height="8" rx="1.5"/><rect x="13" y="5" width="8" height="8" rx="1.5"/><rect x="13" y="15" width="8" height="6" rx="1.5"/>',
 "nap":'<path d="M21 13A8 8 0 1 1 11 3a6 6 0 0 0 10 10z"/>',
 "bath":'<path d="M4 12h16v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M6 12V6a2 2 0 0 1 4 0M17 20l1 2M7 20l-1 2"/>',
 "bed":'<path d="M3 18v-7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v7M3 14h18M5 9V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v3"/>'}
def day_html():
    items="".join('<div class="d"><span class="i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg></span><b>%s</b></div>'%(DAY_ICO[k],t) for k,t in DAY)
    return '<div class="sci-day">'+items+'<div class="d again"><span class="i">↻</span><b>A familiar rhythm, day after day</b></div></div>'

p3_pred = sec("Four · Predictability", 'Familiar routines help your child know <span class="sci-squig">what comes next.</span>',
 "When our team asked Phil Fisher, of the Stanford Center on Early Childhood, what advice he would give parents, he emphasized predictability: familiar routines children can count on.",
 line("Familiar patterns around meals, play, and bedtime can make the day easier to recognize. A routine can be simple and still leave room to adapt.")
 +day_html()
 +take("Keep it simple, familiar, <span class=\"mk\">and flexible.</span>")
 +app_slot("Baby Tracker and the Sleep Habits masterclass", "Keep track of feeds, naps, and diaper changes in one place. Explore bedtime routines in the Sleep Habits masterclass.", "/masterclasses", "See masterclasses"), "#913FA3", "sci26-mint", 1040)
p3_pred = p3_pred.replace('<section class="sci26', '<section id="predictability" class="sci26', 1)

p3_closer = '<section class="sci26 sci26-plain" style="padding:44px 20px 56px"><div class="sci26-wrap" style="max-width:900px;text-align:center"><p class="sci-mantra" style="margin:0">Connect. Guide. Protect. Repeat.</p><p class="sci-line" style="margin-top:18px">Find ideas for putting these principles into practice with your child.</p><p style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px">'+cta("Explore Kinedu", TRY)+cta("Take the free assessment", ASSESS, False)+'</p></div></section>'

page3 = page("/science-what-you-can-do", "So What Can You Do? Four Things in Your Hands | Kinedu",
 "Play, relationships, stress and predictability: the four things the evidence keeps pointing to, and what a parent can actually do with them.",
 "/science-what-you-can-do", p3_hero, [p3_open, p3_play, p3_rel, p3_stress, p3_pred, p3_closer, p3_note, nextprev(("/science-what-we-know","How babies grow"), None)],
 og_title="So what can you do? Four things in your hands | Kinedu")

ARIA={'viewBox="0 0 380 210"':"Share of babies who lift their head while on tummy, by age: 17% at birth, 48% at 3 months, 93% at 5 months",
      'viewBox="0 0 520 260"':"How tightly the four areas move together, by age: 0.49 at 2 months falling to 0.27 at 14 months and staying there",
      'viewBox="0 0 720 280"':"Skills stacked in order: lifts their head at about 3 months, sits at 7, stands at 12, walks at 13",
      'viewBox="0 0 520 300"':"Share of children babbling and saying first words, by age: babbling rises first, first words follow",
      'viewBox="0 0 940 208"':"Range of normal: learning to walk spans 8 to 13 months, dressing and feeding themselves spans 17 to 39 months",
      'viewBox="0 0 720 235"':"Windows: exploring objects 1 to 5 months, first steps 8 to 13 months, first words 14 to 25 months"}
def aria(html):
    for vb,lab in ARIA.items():
        html=re.sub(r'(<svg [^>]*?'+re.escape(vb)+r'[^>]*?role="img")(?![^>]*aria-label)', r'\1 aria-label="'+lab+'"', html)
    return html
import sys; sys.path.insert(0, os.path.dirname(__file__)); from es import to_es; from pt import to_pt
for name,html in [("science.html",page1),("science-what-we-know.html",page2),("science-what-you-can-do.html",page3)]:
    html=aria(html)
    html=re.sub(r"\\?'DM Mono\\?',\s*monospace","inherit",html).replace('font-family="DM Mono,monospace"','font-family="Proxima Nova,Arial,sans-serif"').replace("DM Sans,Arial,sans-serif","Proxima Nova,Arial,sans-serif")
    open(os.path.join(L,name),"w",encoding="utf-8").write(html)
    vis=re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->','',html,flags=re.S); vis=re.sub(r'<[^>]+>','',vis)
    print(name, len(html)//1024,"KB · rayas visibles:", vis.count("—"), "· ' - ':", vis.count(" - "))
    for lang, fn in (("es", to_es), ("pt", to_pt)):
        lhtml, missing = fn(html, "/"+name.replace(".html",""))
        open(os.path.join(L,lang,name),"w",encoding="utf-8").write(lhtml)
        IGN=("Masterclasses","Live Classes","Blog","Gift","Science","Team","Founder","Experts","How's my baby?","Try free","Stanford","MIT","Company","About us","The science","Support","Contact us","Terms & Conditions","Privacy Policy","Recommended by pediatricians. Loved by parents. Built for your baby, exactly as they are right now.","&copy; 2016–2026 Kinedu. All rights reserved.")
        missing=[m for m in missing if m not in IGN and not re.search(r'[áéíóúñãõçÁÉÍÓÚ¿¡]', m)]
        if missing: print("  "+lang+"/"+name, "· sin traducir:", missing[:10])

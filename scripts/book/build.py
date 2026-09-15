#!/usr/bin/env python3
"""Genera /book (EN), /es/book y /pt/book: la página del libro Big Bang Baby.

Toma nav, footer y scripts de {lang}/science.html para que el header y el footer
sean idénticos al resto del sitio. La introducción del libro va textual (en inglés,
el idioma en que está publicado) desde scripts/book/introduction.html y
scripts/book/before-we-begin.html, extraídos del EPUB final.

Uso:  python3 scripts/book/build.py
"""
import re, html, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
AMAZON = "https://www.amazon.com/dp/B0HHL292P6"
SITE = "https://www.kinedu.com"

PRE = (HERE / "before-we-begin.html").read_text(encoding="utf-8")
INTRO = (HERE / "introduction.html").read_text(encoding="utf-8")

def words(s): return len(re.sub(r"<[^>]+>", " ", s).split())
READ_MIN = round((words(PRE) + words(INTRO)) / 230)

C = {
 "en": dict(
  path="/book", src="science.html", base="",
  title="Big Bang Baby, the book by Kinedu’s founder | Kinedu",
  desc="Luis Garza Sada, founder of Kinedu, wrote Big Bang Baby: the science of how your child’s universe takes shape. Read the full introduction and pre-order the book.",
  og_title="Big Bang Baby: the book by Kinedu’s founder",
  nav_item="The book",
  kick="The book by Kinedu’s founder",
  date="Out 23 September 2026", date_after="Out now",
  by="Luis Garza Sada, founder of Kinedu",
  lead="Sixteen years building Kinedu, four daughters, and a record of how 3.5 million children grew. Luis wrote down what all of it taught him about the first years.",
  cta="Pre-order on Amazon", cta_after="Get it on Amazon",
  cta2="Read the introduction",
  fine="Kindle edition, $9.99 USD. Paperback coming soon. Published in English.",
  what_kick="What the book is",
  what_h2='Not a checklist. <span class="bk-squig">A field guide.</span>',
  what_lead="Big Bang Baby restores awe and confidence to parenting: your child is not a checklist to complete, but a universe taking shape. Your loving, imperfect presence is one of the forces that helps hold it together.",
  inside="Inside the book",
  bullets=[
   "Why everyday moments are quietly building everything at once",
   "The difference between a window that narrows and one that slams shut",
   "Why your child is supposed to be different from every other child, including their sibling",
   "The four invisible forces of development: play, relationships, stress, and predictability",
   "How to stop asking whether your child is behind and start asking what they are ready for now",
  ],
  read_kick="From the book",
  read_h2='Read the <span class="bk-squig">introduction.</span>',
  read_note=f"Reproduced from Big Bang Baby. About {READ_MIN} minutes.",
  end_h="The introduction ends here.",
  end_p="The rest is in the book.",
  end_link="More at bigbangbaby.net",
  auth_kick="About the author",
  auth_bio="Luis Garza Sada is a father of four and the founder and CEO of Kinedu, an early-childhood company serving millions of families worldwide. For more than sixteen years, he has worked at the intersection of early childhood, technology, and research. He lives in Monterrey, Mexico, with his wife, Paulina, and their four daughters.",
  auth_link="Meet the founder",
  cover_alt="Big Bang Baby, the book by Luis Garza Sada",
  photo_alt="Luis Garza Sada, author of Big Bang Baby and founder of Kinedu",
 ),
 "es": dict(
  path="/es/book", src="es/science.html", base="/es",
  title="Big Bang Baby, el libro del fundador de Kinedu | Kinedu",
  desc="Luis Garza Sada, fundador de Kinedu, escribió Big Bang Baby: la ciencia de cómo toma forma el universo de tu hijo. Lee la introducción completa y reserva el libro.",
  og_title="Big Bang Baby: el libro del fundador de Kinedu",
  nav_item="El libro",
  kick="El libro del fundador de Kinedu",
  date="Sale el 23 de septiembre de 2026", date_after="Ya disponible",
  by="Luis Garza Sada, fundador de Kinedu",
  lead="Dieciséis años construyendo Kinedu, cuatro hijas y el registro de cómo crecieron 3.5 millones de niños. Luis escribió lo que todo eso le enseñó sobre los primeros años.",
  cta="Reserva en Amazon", cta_after="Cómpralo en Amazon",
  cta2="Lee la introducción",
  fine="Edición Kindle, 9.99 USD. Pasta blanda próximamente. Publicado en inglés.",
  what_kick="Qué es el libro",
  what_h2='No es una lista de pendientes. <span class="bk-squig">Es una guía de campo.</span>',
  what_lead="Big Bang Baby devuelve el asombro y la confianza a la crianza: tu hijo no es una lista por completar, sino un universo tomando forma. Tu presencia, amorosa e imperfecta, es una de las fuerzas que lo sostienen.",
  inside="Dentro del libro",
  bullets=[
   "Por qué los momentos cotidianos construyen todo a la vez, sin que lo notes",
   "La diferencia entre una ventana que se angosta y una que se cierra de golpe",
   "Por qué tu hijo tiene que ser distinto a todos los demás niños, incluidos sus hermanos",
   "Las cuatro fuerzas invisibles del desarrollo: juego, relaciones, estrés y predictibilidad",
   "Cómo dejar de preguntar si tu hijo va atrasado y empezar a preguntar para qué está listo ahora",
  ],
  read_kick="Del libro",
  read_h2='Lee la <span class="bk-squig">introducción.</span>',
  read_note=f"Reproducida de Big Bang Baby. El libro está publicado en inglés, así que la introducción va en su idioma original. Unos {READ_MIN} minutos de lectura.",
  end_h="La introducción termina aquí.",
  end_p="El resto está en el libro.",
  end_link="Más en bigbangbaby.net",
  auth_kick="Sobre el autor",
  auth_bio="Luis Garza Sada es papá de cuatro hijas y fundador y CEO de Kinedu, una empresa de primera infancia que acompaña a millones de familias en todo el mundo. Desde hace más de dieciséis años trabaja en el cruce entre primera infancia, tecnología e investigación. Vive en Monterrey, México, con su esposa, Paulina, y sus cuatro hijas.",
  auth_link="Conoce al fundador",
  cover_alt="Big Bang Baby, el libro de Luis Garza Sada",
  photo_alt="Luis Garza Sada, autor de Big Bang Baby y fundador de Kinedu",
 ),
 "pt": dict(
  path="/pt/book", src="pt/science.html", base="/pt",
  title="Big Bang Baby, o livro do fundador do Kinedu | Kinedu",
  desc="Luis Garza Sada, fundador do Kinedu, escreveu Big Bang Baby: a ciência de como o universo do seu filho toma forma. Leia a introdução completa e reserve o livro.",
  og_title="Big Bang Baby: o livro do fundador do Kinedu",
  nav_item="O livro",
  kick="O livro do fundador do Kinedu",
  date="Lançamento em 23 de setembro de 2026", date_after="Já disponível",
  by="Luis Garza Sada, fundador do Kinedu",
  lead="Dezesseis anos construindo o Kinedu, quatro filhas e o registro de como 3,5 milhões de crianças cresceram. Luis escreveu o que tudo isso lhe ensinou sobre os primeiros anos.",
  cta="Reserve na Amazon", cta_after="Compre na Amazon",
  cta2="Leia a introdução",
  fine="Edição Kindle, US$ 9,99. Brochura em breve. Publicado em inglês.",
  what_kick="O que é o livro",
  what_h2='Não é uma lista de tarefas. <span class="bk-squig">É um guia de campo.</span>',
  what_lead="Big Bang Baby devolve o encanto e a confiança à criação dos filhos: seu filho não é uma lista a completar, e sim um universo tomando forma. Sua presença, amorosa e imperfeita, é uma das forças que o mantêm unido.",
  inside="Dentro do livro",
  bullets=[
   "Por que os momentos do dia a dia constroem tudo ao mesmo tempo, sem que você perceba",
   "A diferença entre uma janela que se estreita e uma que se fecha de repente",
   "Por que seu filho deve ser diferente de todas as outras crianças, inclusive dos irmãos",
   "As quatro forças invisíveis do desenvolvimento: brincadeira, relações, estresse e previsibilidade",
   "Como parar de perguntar se seu filho está atrasado e começar a perguntar para o que ele está pronto agora",
  ],
  read_kick="Do livro",
  read_h2='Leia a <span class="bk-squig">introdução.</span>',
  read_note=f"Reproduzida de Big Bang Baby. O livro é publicado em inglês, por isso a introdução está no idioma original. Cerca de {READ_MIN} minutos de leitura.",
  end_h="A introdução termina aqui.",
  end_p="O resto está no livro.",
  end_link="Mais em bigbangbaby.net",
  auth_kick="Sobre o autor",
  auth_bio="Luis Garza Sada é pai de quatro filhas e fundador e CEO do Kinedu, uma empresa de primeira infância que acompanha milhões de famílias no mundo todo. Há mais de dezesseis anos trabalha na interseção entre primeira infância, tecnologia e pesquisa. Mora em Monterrey, no México, com a esposa, Paulina, e as quatro filhas.",
  auth_link="Conheça o fundador",
  cover_alt="Big Bang Baby, o livro de Luis Garza Sada",
  photo_alt="Luis Garza Sada, autor de Big Bang Baby e fundador do Kinedu",
 ),
}

CSS = r"""
:root{--bk-navy:#0A1A33;--bk-edge:#050D1F;--bk-ink:#EDF1F8;--bk-gold:#E9C77E;--bk-gold-ink:#2A2009;--bk-text:#1A1D2E;--bk-muted:#52607A}
.bk{font-family:'Proxima Nova','Inter',-apple-system,BlinkMacSystemFont,sans-serif;color:var(--bk-text);overflow-x:hidden}
.bk *{box-sizing:border-box}
.bk-wrap{max-width:1040px;margin:0 auto;position:relative;z-index:1}
.bk-kick{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#7A5A1E;background:#FBF3DF;border:1px solid #F0DFB0;border-radius:999px;padding:7px 14px;margin:0 0 18px}
.bk-kick i{width:6px;height:6px;border-radius:50%;background:var(--bk-gold);display:inline-block}
.bk h2{font-size:clamp(1.9rem,3.4vw,2.6rem);line-height:1.12;letter-spacing:-.025em;font-weight:800;color:#081B46;margin:0 0 16px;text-wrap:balance}
.bk-squig{color:#9A7423;position:relative;white-space:nowrap}
.bk-squig::after{content:"";position:absolute;left:2%;right:2%;bottom:-5px;height:9px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='9' viewBox='0 0 28 9'%3E%3Cpath d='M0 5.5 Q 7 1 14 5.5 T 28 5.5' fill='none' stroke='%23E9C77E' stroke-width='2.6' stroke-linecap='round'/%3E%3C/svg%3E") repeat-x;background-size:auto 9px}
.bk-lead{font-size:clamp(1.05rem,1.6vw,1.22rem);line-height:1.6;color:var(--bk-muted);max-width:640px;margin:0;text-wrap:pretty}
.bk-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:999px;padding:16px 30px;font-weight:800;font-size:15.5px;text-decoration:none;transition:transform .15s,box-shadow .15s,background .15s;white-space:nowrap}
.bk-btn:hover{transform:translateY(-2px)}
.bk-btn-gold{background:var(--bk-gold);color:var(--bk-gold-ink);box-shadow:0 18px 40px -16px rgba(233,199,126,.7)}
.bk-btn-gold:hover{background:#F2D48E}
.bk-btn-ghost{background:transparent;color:var(--bk-ink);border:1.5px solid rgba(237,241,248,.45)}
.bk-btn-ghost:hover{border-color:rgba(237,241,248,.9)}
.bk-btn-navy{background:#081B46;color:#fff;box-shadow:0 18px 40px -16px rgba(8,27,70,.6)}
.bk-btn-navy:hover{background:#12264A}
/* ---- hero ---- */
.bk-hero{position:relative;background:radial-gradient(120% 90% at 50% 45%,#12264A 0%,var(--bk-navy) 45%,var(--bk-edge) 100%);color:var(--bk-ink);padding:170px 24px 96px;overflow:hidden}
.bk-hero::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(1.4px 1.4px at 8% 22%,rgba(157,180,214,.9),transparent 60%),radial-gradient(1px 1px at 18% 68%,rgba(157,180,214,.7),transparent 60%),radial-gradient(1.6px 1.6px at 27% 38%,rgba(255,255,255,.75),transparent 60%),radial-gradient(1px 1px at 36% 82%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.2px 1.2px at 44% 14%,rgba(157,180,214,.8),transparent 60%),radial-gradient(1px 1px at 57% 58%,rgba(157,180,214,.55),transparent 60%),radial-gradient(1.8px 1.8px at 66% 24%,rgba(255,255,255,.7),transparent 60%),radial-gradient(1px 1px at 73% 76%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.3px 1.3px at 84% 40%,rgba(157,180,214,.85),transparent 60%),radial-gradient(1px 1px at 92% 66%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.5px 1.5px at 12% 90%,rgba(255,255,255,.55),transparent 60%),radial-gradient(1px 1px at 61% 92%,rgba(157,180,214,.5),transparent 60%),radial-gradient(1.2px 1.2px at 96% 12%,rgba(157,180,214,.7),transparent 60%)}
.bk-hero::after{content:"";position:absolute;left:62%;top:58%;width:820px;height:640px;transform:translate(-50%,-50%);pointer-events:none;background:radial-gradient(circle at center,rgba(255,226,168,.22) 0%,rgba(233,199,126,.15) 18%,rgba(214,168,92,.06) 42%,transparent 66%);filter:blur(10px)}
.bk-hero .bk-wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:56px;align-items:center}
.bk-hero .bk-kick{color:var(--bk-gold);background:rgba(233,199,126,.08);border-color:rgba(233,199,126,.28)}
.bk-hero h1{font-size:clamp(2.6rem,6vw,4.6rem);line-height:.98;letter-spacing:.04em;text-transform:uppercase;font-weight:800;color:#fff;margin:0 0 14px}
.bk-hero .bk-subtitle{font-size:clamp(1.15rem,2vw,1.5rem);line-height:1.35;color:var(--bk-ink);margin:0 0 10px;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
.bk-hero .bk-by{font-size:15px;color:#B9C6DC;margin:0 0 26px;font-weight:600}
.bk-hero .bk-tag{font-size:clamp(1.2rem,2vw,1.45rem);font-style:italic;color:var(--bk-gold);margin:0 0 14px;font-weight:600}
.bk-hero .bk-lead{color:#C9D3E6;margin-bottom:30px}
.bk-hero .bk-ctas{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.bk-hero .bk-fine{font-size:13px;color:#8FA1C0;margin:18px 0 0}
.bk-hero .bk-date{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--bk-gold);margin-left:10px}
.bk-hero .bk-date::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--bk-gold)}
.bk-cover{position:relative;display:flex;justify-content:center}
.bk-cover img{width:100%;max-width:400px;height:auto;display:block;filter:drop-shadow(0 40px 60px rgba(0,0,0,.55))}
/* ---- what ---- */
.bk-what{background:#FBFAF8;padding:88px 24px}
.bk-what .bk-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.bk-inside{background:#fff;border:1px solid #EBE6DF;border-radius:24px;padding:30px 30px 22px;box-shadow:0 24px 60px -40px rgba(8,27,70,.25)}
.bk-inside .lbl{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8A94A8;margin:0 0 14px}
.bk-inside ul{list-style:none;margin:0;padding:0}
.bk-inside li{display:flex;gap:14px;align-items:flex-start;padding:13px 0;border-top:1px solid #F0EDE7;font-size:16px;line-height:1.5;color:#132351;text-wrap:pretty}
.bk-inside li:first-child{border-top:0;padding-top:0}
.bk-inside li .st{flex-shrink:0;width:22px;height:22px;margin-top:1px;color:#C9A44A}
/* ---- read ---- */
.bk-read{background:#fff;padding:88px 24px 72px;border-top:1px solid #F0EDE7}
.bk-read .bk-head{max-width:680px;margin:0 auto 44px}
.bk-read .bk-note{font-size:14px;color:#8A94A8;margin:8px 0 0}
.bk-essay{max-width:680px;margin:0 auto;font-size:19px;line-height:1.72;color:var(--bk-text)}
.bk-essay h2{font-size:clamp(1.6rem,2.6vw,2.05rem);line-height:1.15;letter-spacing:-.02em;margin:0 0 8px;color:#081B46;text-wrap:balance}
.bk-essay h2.bk-h-pre{font-size:1.35rem;margin-bottom:6px}
.bk-essay h3{font-size:1.2rem;line-height:1.3;font-weight:800;color:#081B46;margin:52px 0 14px;letter-spacing:-.01em;text-wrap:balance}
.bk-essay p{margin:0 0 1.15em;text-wrap:pretty}
.bk-essay p.bk-sub{font-size:1.05rem;color:#8A94A8;margin:0 0 30px}
.bk-essay p.bk-sub em{font-style:italic}
.bk-essay strong{color:#081B46}
.bk-essay .bk-pre{background:#FBFAF8;border:1px solid #EBE6DF;border-radius:20px;padding:28px 30px 12px;margin:0 0 48px;font-size:17px;line-height:1.68}
.bk-rule{width:56px;height:2px;background:var(--bk-gold);border-radius:2px;margin:0 auto 40px}
.bk-end{max-width:680px;margin:56px auto 0;background:radial-gradient(120% 120% at 20% 20%,#12264A 0%,var(--bk-navy) 50%,var(--bk-edge) 100%);color:var(--bk-ink);border-radius:26px;padding:34px 36px;display:grid;grid-template-columns:96px 1fr;gap:28px;align-items:center;position:relative;overflow:hidden}
.bk-end::after{content:"";position:absolute;right:-60px;bottom:-120px;width:360px;height:360px;background:radial-gradient(circle,rgba(233,199,126,.28),transparent 65%);filter:blur(8px);pointer-events:none}
.bk-end img{width:96px;height:auto;display:block;filter:drop-shadow(0 18px 24px rgba(0,0,0,.5));position:relative;z-index:1}
.bk-end .t{position:relative;z-index:1}
.bk-end .h{font-size:1.35rem;font-weight:800;color:#fff;margin:0 0 4px;letter-spacing:-.01em}
.bk-end .p{font-size:1rem;color:#C9D3E6;margin:0 0 18px}
.bk-end .bk-ctas{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center}
.bk-end .bk-more{color:var(--bk-gold);font-weight:700;font-size:14.5px;text-decoration:none;border-bottom:1px solid rgba(233,199,126,.4)}
.bk-end .bk-more:hover{border-bottom-color:var(--bk-gold)}
/* ---- author ---- */
.bk-author{background:#FBFAF8;padding:80px 24px 96px;border-top:1px solid #F0EDE7}
.bk-author .bk-wrap{display:grid;grid-template-columns:200px 1fr;gap:44px;align-items:center;max-width:860px}
.bk-author img{width:200px;height:200px;border-radius:50%;object-fit:cover;display:block;box-shadow:0 24px 50px -24px rgba(8,27,70,.45)}
.bk-author .name{font-size:1.5rem;font-weight:800;color:#081B46;margin:0 0 10px;letter-spacing:-.02em}
.bk-author p{font-size:17px;line-height:1.62;color:var(--bk-muted);margin:0 0 18px;text-wrap:pretty}
.bk-author a.lnk{color:#087BF3;font-weight:700;text-decoration:none;font-size:15.5px}
.bk-author a.lnk:hover{text-decoration:underline}
@media(max-width:900px){
  .bk-hero{padding:130px 20px 64px}
  .bk-hero .bk-wrap{grid-template-columns:1fr;gap:36px}
  .bk-hero .bk-cover{order:-1}
  .bk-cover img{max-width:230px}
  .bk-hero h1{font-size:clamp(2.3rem,10vw,3rem)}
  .bk-hero .bk-ctas .bk-btn{width:100%}
  .bk-hero .bk-date{margin:12px 0 0;display:flex}
  .bk-what,.bk-read,.bk-author{padding:56px 20px}
  .bk-what .bk-grid{grid-template-columns:1fr;gap:28px}
  .bk-inside{padding:22px 20px 14px}
  .bk-essay{font-size:17.5px;line-height:1.7}
  .bk-essay .bk-pre{padding:22px 20px 8px;font-size:16px}
  .bk-essay h3{margin-top:40px}
  .bk-end{grid-template-columns:1fr;padding:26px 22px;text-align:center;justify-items:center}
  .bk-end .bk-ctas{justify-content:center}
  .bk-author .bk-wrap{grid-template-columns:1fr;text-align:center;justify-items:center;gap:22px}
  .bk-author img{width:150px;height:150px}
}
"""

STAR = '<svg class="st" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.3 6.4 6.7.3-5.3 4.2 1.9 6.5L12 16.2l-5.6 3.7 1.9-6.5L3 9.2l6.7-.3z"/></svg>'

LAUNCH_JS = """<script>(function(){if(Date.now()<Date.parse('2026-09-23T06:00:00Z'))return;document.querySelectorAll('[data-after]').forEach(function(e){e.textContent=e.getAttribute('data-after')});})();</script>"""

def essay_html(lang):
    pre = PRE.replace("<h1>", '<h2 class="bk-h-pre">').replace("</h1>", "</h2>")
    intro = INTRO.replace("<h2>", "<h3>").replace("</h2>", "</h3>")
    intro = intro.replace("<h1>", "<h2>", 1).replace("</h1>", "</h2>", 1)
    intro = intro.replace("<p>What This Book Is Not:</p>\n", "", 1)
    intro = intro.replace("<p><em>The Forces Within Us</em></p>", '<p class="bk-sub"><em>The Forces Within Us</em></p>', 1)
    return f'<div class="bk-pre" lang="en">\n{pre}</div>\n<div lang="en">\n{intro}</div>'

def build(lang):
    c = C[lang]
    src = (ROOT / c["src"]).read_text(encoding="utf-8")
    head = re.search(r"<head>(.*?)</head>", src, re.S).group(1)
    tracking = head[: head.find('<meta charset="UTF-8">')].strip()
    nav = re.search(r'<nav class="navbar" id="navbar">.*?</nav>', src, re.S).group(0)
    footer = re.search(r"<footer class=\"footer\">.*?</footer>", src, re.S).group(0)
    tail = src[src.rfind("</footer>") + len("</footer>"):]
    tail = tail[: tail.rfind("</body>")]
    # nav: Science stays open/active, the active item is the book (not part 1)
    base = c["base"]
    nav = nav.replace(f'href="{base}/science" class="nd-item is-active"', f'href="{base}/science" class="nd-item"')
    third = re.search(rf'<a href="{re.escape(base)}/science-what-you-can-do" class="nd-item[^"]*" role="menuitem"><span>[^<]*</span></a>', nav).group(0)
    book_item = f'<a href="{base}/book" class="nd-item is-active" role="menuitem"><span>{c["nav_item"]}</span></a>'
    nav = re.sub(rf'<a href="{re.escape(base)}/book" class="nd-item[^"]*" role="menuitem"><span>[^<]*</span></a>', '', nav)  # el nav fuente ya trae el ítem; lo reponemos como activo
    nav = nav.replace(third, third + book_item, 1)
    assert 'class="nav-dropdown-toggle active"' in nav

    og = "/og-book.png" if lang == "en" else f"/og-book-{lang}.png"
    url = SITE + c["path"]
    ld = {
        "@context": "https://schema.org", "@type": "Book",
        "name": "Big Bang Baby",
        "alternateName": "Big Bang Baby: The Science of How Your Child’s Universe Takes Shape",
        "author": {"@type": "Person", "name": "Luis Garza Sada", "url": SITE + "/founder"},
        "publisher": {"@type": "Organization", "name": "Garza Jasso Press"},
        "isbn": "979-8-9967408-1-9", "bookFormat": "https://schema.org/EBook",
        "datePublished": "2026-09-23", "inLanguage": "en",
        "image": SITE + "/images/book/cover.webp", "url": url,
        "sameAs": ["https://bigbangbaby.net/", AMAZON],
        "offers": {"@type": "Offer", "price": "9.99", "priceCurrency": "USD", "url": AMAZON, "availability": "https://schema.org/PreOrder"},
    }
    bullets = "".join(f"<li>{STAR}<span>{html.escape(b)}</span></li>" for b in c["bullets"])
    lang_attr = {"en": "en", "es": "es", "pt": "pt-BR"}[lang]
    hero_kick = html.escape(c["kick"])
    page = f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="utf-8">
{tracking}
    <meta name="apple-itunes-app" content="app-id=741277284">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(c["title"])}</title>
<meta name="description" content="{html.escape(c["desc"])}">
    <link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}/book">
<link rel="alternate" hreflang="es" href="{SITE}/es/book">
<link rel="alternate" hreflang="pt" href="{SITE}/pt/book">
<link rel="alternate" hreflang="x-default" href="{SITE}/book">
<meta property="og:title" content="{html.escape(c["og_title"])}">
<meta property="og:description" content="{html.escape(c["desc"])}">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta property="og:type" content="book">
<meta property="og:site_name" content="Kinedu">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(c["og_title"])}">
<meta name="twitter:description" content="{html.escape(c["desc"])}">
<meta name="twitter:image" content="{SITE}{og}">
    <link rel="preload" href="/fonts/proxima-nova/proximanova-regular-webfont.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonts/proxima-nova/proximanova-bold-webfont.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/images/book/cover-3d.webp" as="image" type="image/webp">
    <link rel="stylesheet" href="/styles.css?v=0842a">
    <link rel="icon" href="/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{nav}
<main class="bk">
<section class="bk-hero">
  <div class="bk-wrap">
    <div>
      <span class="bk-kick"><i></i>{hero_kick}</span>
      <h1>Big Bang Baby</h1>
      <p class="bk-subtitle" lang="en">The Science of How Your Child’s Universe Takes Shape</p>
      <p class="bk-by">{html.escape(c["by"])}</p>
      <p class="bk-tag" lang="en">Every child is a universe being born.</p>
      <p class="bk-lead">{html.escape(c["lead"])}</p>
      <div class="bk-ctas">
        <a class="bk-btn bk-btn-gold" href="{AMAZON}" target="_blank" rel="noopener" data-after="{html.escape(c["cta_after"])}">{html.escape(c["cta"])}</a>
        <a class="bk-btn bk-btn-ghost" href="#introduction">{html.escape(c["cta2"])}</a>
        <span class="bk-date" data-after="{html.escape(c["date_after"])}">{html.escape(c["date"])}</span>
      </div>
      <p class="bk-fine">{html.escape(c["fine"])}</p>
    </div>
    <div class="bk-cover">
      <img src="/images/book/cover-3d.webp" srcset="/images/book/cover-3d-sm.webp 420w, /images/book/cover-3d.webp 724w" sizes="(max-width: 900px) 230px, 400px" width="724" height="1179" alt="{html.escape(c["cover_alt"])}" fetchpriority="high">
    </div>
  </div>
</section>
<section class="bk-what">
  <div class="bk-wrap bk-grid">
    <div>
      <span class="bk-kick"><i></i>{html.escape(c["what_kick"])}</span>
      <h2>{c["what_h2"]}</h2>
      <p class="bk-lead">{html.escape(c["what_lead"])}</p>
    </div>
    <div class="bk-inside">
      <p class="lbl">{html.escape(c["inside"])}</p>
      <ul>{bullets}</ul>
    </div>
  </div>
</section>
<section class="bk-read" id="introduction">
  <div class="bk-head">
    <span class="bk-kick"><i></i>{html.escape(c["read_kick"])}</span>
    <h2>{c["read_h2"]}</h2>
    <p class="bk-note">{html.escape(c["read_note"])}</p>
  </div>
  <div class="bk-rule"></div>
  <article class="bk-essay">
{essay_html(lang)}
  </article>
  <aside class="bk-end">
    <img src="/images/book/cover-3d-sm.webp" width="96" height="156" alt="" loading="lazy">
    <div class="t">
      <p class="h">{html.escape(c["end_h"])}</p>
      <p class="p">{html.escape(c["end_p"])}</p>
      <div class="bk-ctas">
        <a class="bk-btn bk-btn-gold" href="{AMAZON}" target="_blank" rel="noopener" data-after="{html.escape(c["cta_after"])}">{html.escape(c["cta"])}</a>
        <a class="bk-more" href="https://bigbangbaby.net/" target="_blank" rel="noopener">{html.escape(c["end_link"])}</a>
      </div>
    </div>
  </aside>
</section>
<section class="bk-author">
  <div class="bk-wrap">
    <img src="/images/book/luis-garza-sada.webp" width="200" height="200" alt="{html.escape(c["photo_alt"])}">
    <div>
      <span class="bk-kick"><i></i>{html.escape(c["auth_kick"])}</span>
      <p class="name">Luis Garza Sada</p>
      <p>{html.escape(c["auth_bio"])}</p>
      <a class="lnk" href="/founder">{html.escape(c["auth_link"])} →</a>
    </div>
  </div>
</section>
</main>
{footer}
{tail.strip()}
{LAUNCH_JS}
</body>
</html>
"""
    out = ROOT / (c["path"].lstrip("/") + ".html")
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT), len(page) // 1024, "KB")

if __name__ == "__main__":
    for lang in ("en", "es", "pt"):
        build(lang)

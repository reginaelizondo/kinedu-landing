#!/usr/bin/env python3
"""Genera /book (EN), /es/book y /pt/book: la landing del libro Big Bang Baby.

Toma nav, footer y scripts de {lang}/science.html para que el header y el footer
sean idénticos al resto del sitio. Las frases del libro van textuales en inglés
(el idioma en que está publicado); el resto del copy se traduce.

Uso:  python3 scripts/book/build.py
"""
import re, html, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
AMAZON = "https://www.amazon.com/dp/B0HHL292P6"
SITE = "https://www.kinedu.com"

# Frases textuales del libro (banco de frases del kit + introducción). No se traducen.
Q_TAG = "Every child is a universe being born."
Q_BEGIN = "In the beginning, everything is everything."
Q_EARLIER = "Earlier is better; later is not impossible."
Q_WINDOW = "The window narrows; it does not slam shut."
Q_WATCH = "Watch the child, not the chart."
Q_RANGE = "The range of normal is astonishingly wide."
EXCERPT = ("It looks like a father sitting on the kitchen floor at 7:15 in the morning, trying to make the school carpool on time while running late for work, “holding space” for a three-year-old who is screaming because her banana broke in half. "
           "The father knows, somewhere deep in the rational part of his brain, that this is developmentally normal. He has read the posts. He understands that a three-year-old does not yet have the capacity to regulate an intense emotional response. He is trying to do the right thing.")
BLURB = "Big Bang Baby restores awe and confidence to parenting: your child is not a checklist to complete, but a universe taking shape — and your loving, imperfect presence is one of the forces that helps hold it together."  # blurb oficial del libro, tal cual bigbangbaby.net (Regina: dejarlo así)
BIO = "Luis Garza Sada is a father of four and an early-childhood practitioner. For more than sixteen years he has worked at the intersection of parenting, technology, and developmental science — as the founder and CEO of Kinedu, an early childhood company serving millions of families, and in partnership with researchers at Stanford and the Harvard Center on the Developing Child. He lives in Monterrey, Mexico, with his wife, Paulina, and their four daughters. He has been recognized as an EY Entrepreneur Of The Year and is part of the global Endeavor network of entrepreneurs."  # bio oficial, tal cual bigbangbaby.net (Regina: dejarlo así)
EXCERPT2 = "Meanwhile, three other children need breakfast, school starts in twenty minutes, and the broken banana is now on the floor."

C = {
 "en": dict(
  path="/book", src="science.html", base="",
  title="Big Bang Baby, the book by Kinedu’s founder | Kinedu",
  desc="Luis Garza Sada, founder of Kinedu, wrote Big Bang Baby: the science of how your child’s universe takes shape. Why your baby grows like the universe, and what that changes for you.",
  og_title="Big Bang Baby: the book by Kinedu’s founder",
  kick="The book by Kinedu’s founder",
  date="Out 23 September 2026", date_after="Out now",
  by="Luis Garza Sada, founder of Kinedu",
  lead="What sixteen years of Kinedu, four daughters and the record of 3.5 million children taught Luis about the first years.",
  cta="Pre-order on Amazon", cta_after="Get it on Amazon",
  cta2="See what’s inside",
  stats=[("3.5M", "children in the data"), ("16", "years building Kinedu"), ("4", "daughters, all the field testing")],
  fine="Kindle edition, $9.99 USD. Paperback coming soon. Published in English.",
  idea_kick="The big idea",
  idea_h2='Your baby grows like <span class="bk-squig">the universe.</span>',
  idea_lead="Mind, body, language and emotions are not four separate tracks. Early on they move together. Then they expand, cool, and take shape.",
  idea=[
   (Q_BEGIN, "In the first months every skill touches every other one. A game of peekaboo is building language, memory and trust at the same time."),
   ("It expands.", "Connections multiply faster than at any other time in life. Windows open. " + Q_EARLIER),
   ("It takes shape.", "Around the first birthday, distinct areas emerge and your child starts becoming exactly who they are. Different from every other child, including their sibling."),
  ],
  idea_note="Seen in the record of 3.5 million children who grew up with Kinedu.",
  why_kick="Why this book",
  why_h2='Parenting advice got loud. <span class="bk-squig">This is the calm.</span>',
  why_lead="Contradictory experts, vague slogans, and the fear that one wrong move lasts forever. Luis lived it too, four daughters deep.",
  excerpt_lbl="From the introduction",
  conv=[
   ("You are the adult in the room.", "Warmth and structure together, not one or the other. Setting a limit does not break the bond."),
   ("All feelings are real. Not every reaction is valid.", "Helping your child feel an emotion is not the same as accepting whatever that emotion makes them do."),
   ("A bad day is not trauma.", "Normal friction builds resilience. What makes stress safe is a caring adult nearby. That adult is you."),
  ],
  inside_kick="Inside the book",
  inside_h2='Three parts. <span class="bk-squig">One map.</span>',
  inside_lead="Not a manual, not a checklist. A way to see your own child clearly, age by age.",
  parts=[
   ("The Old Cosmology", "What the classic theories of child development got right, what they missed, and why it still costs parents clarity today."),
   ("The Big Bang", "The first year: everything coupled, then an explosion of new capacities. Why the windows narrow but do not slam shut."),
   ("The Universe Takes Shape", "Distinct areas emerge, age by age. And the four invisible forces that hold it all together."),
  ],
  part_lbl=["Part 1", "Part 2", "Part 3"],
  extras="Plus a parent’s guide to the Kinedu report, a glossary in plain language, and a research primer.",
  who_lbl="Who it’s for",
  who=["New and expecting parents who want science without the guilt trip", "Anyone tired of advice that contradicts itself every Tuesday", "Educators and pediatric professionals who want one framework, not ten tribes"],
  close_h2="You were there for the Big Bang. Be there for the rest.",
  close_p="Kindle edition out 23 September 2026. Paperback coming soon.",
  end_link="More at bigbangbaby.net",
  auth_kick="About the author",
  auth_bio="Luis Garza Sada is a father of four and the founder and CEO of Kinedu, an early-childhood company serving millions of families worldwide. For more than sixteen years, he has worked at the intersection of early childhood, technology, and research. He lives in Monterrey, Mexico, with his wife, Paulina, and their four daughters.",
  auth_link="Meet the founder",
  cover_alt="Big Bang Baby, the book by Luis Garza Sada",
  photo_alt="Luis Garza Sada, author of Big Bang Baby and founder of Kinedu",
  en_note="",
 ),
 "es": dict(
  path="/es/book", src="es/science.html", base="/es",
  title="Big Bang Baby, el libro del fundador de Kinedu | Kinedu",
  desc="Luis Garza Sada, fundador de Kinedu, escribió Big Bang Baby: la ciencia de cómo toma forma el universo de tu hijo. Por qué tu bebé crece como el universo y qué cambia eso para ti.",
  og_title="Big Bang Baby: el libro del fundador de Kinedu",
  kick="El libro del fundador de Kinedu",
  date="Sale el 23 de septiembre de 2026", date_after="Ya disponible",
  by="Luis Garza Sada, fundador de Kinedu",
  lead="Lo que dieciséis años de Kinedu, cuatro hijas y el registro de 3.5 millones de niños le enseñaron a Luis sobre los primeros años.",
  cta="Reserva en Amazon", cta_after="Cómpralo en Amazon",
  cta2="Mira qué trae",
  stats=[("3.5M", "niños en los datos"), ("16", "años construyendo Kinedu"), ("4", "hijas, todas las pruebas de campo")],
  fine="Edición Kindle, 9.99 USD. Pasta blanda próximamente. Publicado en inglés.",
  idea_kick="La gran idea",
  idea_h2='Tu bebé crece como <span class="bk-squig">el universo.</span>',
  idea_lead="Mente, cuerpo, lenguaje y emociones no son cuatro carriles separados. Al principio se mueven juntos. Después se expanden, se enfrían y toman forma.",
  idea=[
   (Q_BEGIN, "En los primeros meses cada habilidad toca a todas las demás. Un juego de “¿dónde está?” construye lenguaje, memoria y confianza al mismo tiempo."),
   ("Se expande.", "Las conexiones se multiplican más rápido que en cualquier otro momento de la vida. Se abren ventanas. Antes es mejor; después no es imposible."),
   ("Toma forma.", "Cerca del primer cumpleaños aparecen áreas distintas y tu hijo empieza a ser exactamente quien es. Distinto a todos los demás niños, incluidos sus hermanos."),
  ],
  idea_note="Visto en el registro de 3.5 millones de niños que crecieron con Kinedu.",
  why_kick="Por qué este libro",
  why_h2='Los consejos de crianza se volvieron ruido. <span class="bk-squig">Esto es la calma.</span>',
  why_lead="Expertos que se contradicen, frases vacías y el miedo a que un error dure para siempre. Luis también lo vivió, con cuatro hijas.",
  excerpt_lbl="De la introducción (en inglés)",
  conv=[
   ("Tú eres el adulto en la habitación.", "Calidez y estructura juntas, no una u otra. Poner un límite no rompe el vínculo."),
   ("Todas las emociones son reales. No todas las reacciones son válidas.", "Ayudar a tu hijo a sentir una emoción no es lo mismo que aceptar cualquier cosa que haga con ella."),
   ("Un mal día no es trauma.", "La fricción normal construye resiliencia. Lo que vuelve seguro el estrés es un adulto que cuida, cerca. Ese adulto eres tú."),
  ],
  inside_kick="Dentro del libro",
  inside_h2='Tres partes. <span class="bk-squig">Un mapa.</span>',
  inside_lead="No es un manual ni una lista de pendientes. Es una forma de ver con claridad a tu propio hijo, edad por edad.",
  parts=[
   ("The Old Cosmology", "Qué acertaron las teorías clásicas del desarrollo infantil, qué se les escapó y por qué eso todavía les cuesta claridad a los papás."),
   ("The Big Bang", "El primer año: todo conectado y luego una explosión de capacidades nuevas. Por qué las ventanas se angostan pero no se cierran de golpe."),
   ("The Universe Takes Shape", "Aparecen áreas distintas, edad por edad. Y las cuatro fuerzas invisibles que lo sostienen todo."),
  ],
  part_lbl=["Parte 1", "Parte 2", "Parte 3"],
  extras="Además: una guía para papás del reporte de Kinedu, un glosario en lenguaje sencillo y un resumen de la investigación.",
  who_lbl="Para quién es",
  who=["Papás nuevos o en espera que quieren ciencia sin culpa", "Cualquiera cansado de consejos que se contradicen cada martes", "Educadores y profesionales de pediatría que quieren un solo marco, no diez tribus"],
  close_h2="You were there for the Big Bang. Be there for the rest.",
  close_p="Edición Kindle el 23 de septiembre de 2026. Pasta blanda próximamente.",
  end_link="Más en bigbangbaby.net",
  auth_kick="Sobre el autor",
  auth_bio="Luis Garza Sada es papá de cuatro hijas y fundador y CEO de Kinedu, una empresa de primera infancia que acompaña a millones de familias en todo el mundo. Desde hace más de dieciséis años trabaja en el cruce entre primera infancia, tecnología e investigación. Vive en Monterrey, México, con su esposa, Paulina, y sus cuatro hijas.",
  auth_link="Conoce al fundador",
  cover_alt="Big Bang Baby, el libro de Luis Garza Sada",
  photo_alt="Luis Garza Sada, autor de Big Bang Baby y fundador de Kinedu",
  en_note="El libro está publicado en inglés.",
 ),
 "pt": dict(
  path="/pt/book", src="pt/science.html", base="/pt",
  title="Big Bang Baby, o livro do fundador do Kinedu | Kinedu",
  desc="Luis Garza Sada, fundador do Kinedu, escreveu Big Bang Baby: a ciência de como o universo do seu filho toma forma. Por que seu bebê cresce como o universo e o que isso muda para você.",
  og_title="Big Bang Baby: o livro do fundador do Kinedu",
  kick="O livro do fundador do Kinedu",
  date="Lançamento em 23 de setembro de 2026", date_after="Já disponível",
  by="Luis Garza Sada, fundador do Kinedu",
  lead="O que dezesseis anos de Kinedu, quatro filhas e o registro de 3,5 milhões de crianças ensinaram a Luis sobre os primeiros anos.",
  cta="Reserve na Amazon", cta_after="Compre na Amazon",
  cta2="Veja o que tem dentro",
  stats=[("3,5M", "crianças nos dados"), ("16", "anos construindo o Kinedu"), ("4", "filhas, todos os testes de campo")],
  fine="Edição Kindle, US$ 9,99. Brochura em breve. Publicado em inglês.",
  idea_kick="A grande ideia",
  idea_h2='Seu bebê cresce como <span class="bk-squig">o universo.</span>',
  idea_lead="Mente, corpo, linguagem e emoções não são quatro trilhas separadas. No começo, elas se movem juntas. Depois se expandem, esfriam e tomam forma.",
  idea=[
   (Q_BEGIN, "Nos primeiros meses, cada habilidade toca todas as outras. Uma brincadeira de esconde-esconde constrói linguagem, memória e confiança ao mesmo tempo."),
   ("Ele se expande.", "As conexões se multiplicam mais rápido do que em qualquer outro momento da vida. Janelas se abrem. Antes é melhor; depois não é impossível."),
   ("Ele toma forma.", "Perto do primeiro aniversário, áreas distintas aparecem e seu filho começa a ser exatamente quem é. Diferente de todas as outras crianças, inclusive dos irmãos."),
  ],
  idea_note="Visto no registro de 3,5 milhões de crianças que cresceram com o Kinedu.",
  why_kick="Por que este livro",
  why_h2='Os conselhos sobre criação viraram barulho. <span class="bk-squig">Isto é a calma.</span>',
  why_lead="Especialistas que se contradizem, frases vazias e o medo de que um erro dure para sempre. Luis também viveu isso, com quatro filhas.",
  excerpt_lbl="Da introdução (em inglês)",
  conv=[
   ("Você é o adulto da casa.", "Carinho e estrutura juntos, não um ou outro. Colocar um limite não quebra o vínculo."),
   ("Todas as emoções são reais. Nem toda reação é válida.", "Ajudar seu filho a sentir uma emoção não é o mesmo que aceitar qualquer coisa que ele faça com ela."),
   ("Um dia ruim não é trauma.", "O atrito normal constrói resiliência. O que torna o estresse seguro é um adulto que cuida, por perto. Esse adulto é você."),
  ],
  inside_kick="Dentro do livro",
  inside_h2='Três partes. <span class="bk-squig">Um mapa.</span>',
  inside_lead="Não é um manual nem uma lista de tarefas. É um jeito de enxergar seu próprio filho com clareza, idade por idade.",
  parts=[
   ("The Old Cosmology", "O que as teorias clássicas do desenvolvimento infantil acertaram, o que deixaram passar e por que isso ainda custa clareza aos pais."),
   ("The Big Bang", "O primeiro ano: tudo conectado e depois uma explosão de novas capacidades. Por que as janelas se estreitam, mas não se fecham de repente."),
   ("The Universe Takes Shape", "Áreas distintas aparecem, idade por idade. E as quatro forças invisíveis que sustentam tudo."),
  ],
  part_lbl=["Parte 1", "Parte 2", "Parte 3"],
  extras="Além disso: um guia para pais do relatório do Kinedu, um glossário em linguagem simples e um resumo da pesquisa.",
  who_lbl="Para quem é",
  who=["Pais novos ou à espera que querem ciência sem culpa", "Qualquer pessoa cansada de conselhos que se contradizem toda terça-feira", "Educadores e profissionais de pediatria que querem um único modelo, não dez tribos"],
  close_h2="You were there for the Big Bang. Be there for the rest.",
  close_p="Edição Kindle em 23 de setembro de 2026. Brochura em breve.",
  end_link="Mais em bigbangbaby.net",
  auth_kick="Sobre o autor",
  auth_bio="Luis Garza Sada é pai de quatro filhas e fundador e CEO do Kinedu, uma empresa de primeira infância que acompanha milhões de famílias no mundo todo. Há mais de dezesseis anos trabalha na interseção entre primeira infância, tecnologia e pesquisa. Mora em Monterrey, no México, com a esposa, Paulina, e as quatro filhas.",
  auth_link="Conheça o fundador",
  cover_alt="Big Bang Baby, o livro de Luis Garza Sada",
  photo_alt="Luis Garza Sada, autor de Big Bang Baby e fundador do Kinedu",
  en_note="O livro é publicado em inglês.",
 ),
}

CSS = r"""
:root{--bk-navy:#0A1A33;--bk-edge:#050D1F;--bk-ink:#EDF1F8;--bk-gold:#E9C77E;--bk-gold-ink:#2A2009;--bk-text:#1A1D2E;--bk-muted:#52607A}
.bk{font-family:'Proxima Nova','Inter',-apple-system,BlinkMacSystemFont,sans-serif;color:var(--bk-text);overflow-x:hidden}
.bk *{box-sizing:border-box}
.bk-wrap{max-width:1040px;margin:0 auto;position:relative;z-index:1}
.bk-sec{padding:88px 24px}
.bk-sec.greige{background:#FBFAF8}
.bk-sec.white{background:#fff;border-top:1px solid #F0EDE7}
.bk-head{text-align:center;max-width:760px;margin:0 auto 40px}
.bk-kick{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#7A5A1E;background:#FBF3DF;border:1px solid #F0DFB0;border-radius:999px;padding:7px 14px;margin:0 0 18px}
.bk-kick i{width:6px;height:6px;border-radius:50%;background:var(--bk-gold);display:inline-block}
.bk h2{font-size:clamp(1.9rem,3.4vw,2.6rem);line-height:1.12;letter-spacing:-.025em;font-weight:800;color:#081B46;margin:0 0 16px;text-wrap:balance}
.bk-squig{color:#9A7423;position:relative;white-space:nowrap}
.bk-squig::after{content:"";position:absolute;left:2%;right:2%;bottom:-5px;height:9px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='9' viewBox='0 0 28 9'%3E%3Cpath d='M0 5.5 Q 7 1 14 5.5 T 28 5.5' fill='none' stroke='%23E9C77E' stroke-width='2.6' stroke-linecap='round'/%3E%3C/svg%3E") repeat-x;background-size:auto 9px}
.bk-lead{font-size:clamp(1.05rem,1.6vw,1.22rem);line-height:1.6;color:var(--bk-muted);max-width:640px;margin:0 auto;text-wrap:pretty}
.bk-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:999px;padding:16px 30px;font-weight:800;font-size:15.5px;text-decoration:none;transition:transform .15s,box-shadow .15s,background .15s;white-space:nowrap}
.bk-btn:hover{transform:translateY(-2px)}
.bk-btn-gold{background:var(--bk-gold);color:var(--bk-gold-ink);box-shadow:0 18px 40px -16px rgba(233,199,126,.7)}
.bk-btn-gold:hover{background:#F2D48E}
.bk-btn-ghost{background:transparent;color:var(--bk-ink);border:1.5px solid rgba(237,241,248,.45)}
.bk-btn-ghost:hover{border-color:rgba(237,241,248,.9)}
/* ---- hero ---- */
.bk-hero{position:relative;background:radial-gradient(120% 90% at 50% 45%,#12264A 0%,var(--bk-navy) 45%,var(--bk-edge) 100%);color:var(--bk-ink);padding:170px 24px 84px;overflow:hidden}
.bk-stars::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(1.4px 1.4px at 8% 22%,rgba(157,180,214,.9),transparent 60%),radial-gradient(1px 1px at 18% 68%,rgba(157,180,214,.7),transparent 60%),radial-gradient(1.6px 1.6px at 27% 38%,rgba(255,255,255,.75),transparent 60%),radial-gradient(1px 1px at 36% 82%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.2px 1.2px at 44% 14%,rgba(157,180,214,.8),transparent 60%),radial-gradient(1px 1px at 57% 58%,rgba(157,180,214,.55),transparent 60%),radial-gradient(1.8px 1.8px at 66% 24%,rgba(255,255,255,.7),transparent 60%),radial-gradient(1px 1px at 73% 76%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.3px 1.3px at 84% 40%,rgba(157,180,214,.85),transparent 60%),radial-gradient(1px 1px at 92% 66%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.5px 1.5px at 12% 90%,rgba(255,255,255,.55),transparent 60%),radial-gradient(1px 1px at 61% 92%,rgba(157,180,214,.5),transparent 60%),radial-gradient(1.2px 1.2px at 96% 12%,rgba(157,180,214,.7),transparent 60%)}
.bk-hero::after{content:"";position:absolute;left:62%;top:58%;width:820px;height:640px;transform:translate(-50%,-50%);pointer-events:none;background:radial-gradient(circle at center,rgba(255,226,168,.22) 0%,rgba(233,199,126,.15) 18%,rgba(214,168,92,.06) 42%,transparent 66%);filter:blur(10px)}
.bk-hero .bk-wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:56px;align-items:center}
.bk-hero .bk-kick{color:var(--bk-gold);background:rgba(233,199,126,.08);border-color:rgba(233,199,126,.28)}
.bk-hero h1{font-size:clamp(2.6rem,6vw,4.6rem);line-height:.98;letter-spacing:.04em;text-transform:uppercase;font-weight:800;color:#fff;margin:0 0 14px}
.bk-hero .bk-subtitle{font-size:clamp(1.15rem,2vw,1.5rem);line-height:1.35;color:var(--bk-ink);margin:0 0 10px;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
.bk-hero .bk-by{font-size:15px;color:#B9C6DC;margin:0 0 24px;font-weight:600}
.bk-hero .bk-tag{font-size:clamp(1.2rem,2vw,1.45rem);font-style:italic;color:var(--bk-gold);margin:0 0 12px;font-weight:600}
.bk-hero .bk-lead{color:#C9D3E6;margin:0 0 28px}
.bk-ctas{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.bk-date{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--bk-gold);margin-left:10px}
.bk-date::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--bk-gold)}
.bk-stats{display:flex;gap:28px;margin:30px 0 0;padding:22px 0 0;border-top:1px solid rgba(237,241,248,.14);flex-wrap:wrap}
.bk-stat .n{font-size:28px;font-weight:800;letter-spacing:-.03em;color:#fff;line-height:1}
.bk-stat .l{font-size:13px;color:#8FA1C0;margin-top:6px;font-weight:600}
.bk-hero .bk-fine{font-size:13px;color:#8FA1C0;margin:22px 0 0}
.bk-cover{position:relative;display:flex;justify-content:center}
.bk-cover img{width:100%;max-width:400px;height:auto;display:block;filter:drop-shadow(0 40px 60px rgba(0,0,0,.55))}
/* ---- cards ---- */
.bk-3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.bk-card{background:#fff;border:1px solid #EBE6DF;border-radius:22px;padding:24px;position:relative;transition:transform .18s ease,box-shadow .18s ease}
.bk-card:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(8,27,70,.08)}
.bk-card .t{font-size:18px;font-weight:800;color:#081B46;margin:0 0 8px;letter-spacing:-.01em;text-wrap:balance}
.bk-card p{font-size:15px;line-height:1.58;color:var(--bk-muted);margin:0;text-wrap:pretty}
.bk-viz{height:120px;border-radius:16px;background:radial-gradient(120% 100% at 50% 50%,#12264A 0%,var(--bk-navy) 60%,var(--bk-edge) 100%);position:relative;overflow:hidden;margin:0 0 18px}
.bk-viz i{position:absolute;border-radius:50%}
.bk-viz.v1 i.c{left:50%;top:50%;width:14px;height:14px;transform:translate(-50%,-50%);background:#FDF6E3;box-shadow:0 0 18px 8px rgba(233,199,126,.55),0 0 50px 24px rgba(233,199,126,.18)}
.bk-viz.v2 i.c{left:50%;top:50%;width:12px;height:12px;transform:translate(-50%,-50%);background:#FDF6E3;box-shadow:0 0 14px 6px rgba(233,199,126,.5)}
.bk-viz.v2 i.r{left:50%;top:50%;transform:translate(-50%,-50%);border:1px solid rgba(233,199,126,.55)}
.bk-viz.v2 i.r1{width:44px;height:44px}.bk-viz.v2 i.r2{width:78px;height:78px;border-color:rgba(233,199,126,.32)}.bk-viz.v2 i.r3{width:112px;height:112px;border-color:rgba(233,199,126,.16)}
.bk-viz.v3 i{width:16px;height:16px;box-shadow:0 0 12px 3px rgba(255,255,255,.12)}
.bk-viz.v3 i.a{left:34%;top:30%;background:#2B8BE4}.bk-viz.v3 i.b{left:60%;top:26%;background:#4CD964}.bk-viz.v3 i.c3{left:40%;top:62%;background:#E84D8A}.bk-viz.v3 i.d{left:64%;top:60%;background:#FFC033}
.bk-viz.v3 i.g{left:50%;top:50%;width:70px;height:70px;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(233,199,126,.22),transparent 70%)}
.bk-note{font-size:13.5px;color:#8A94A8;text-align:center;margin:22px 0 0}
/* ---- blurb ---- */
.bk-blurb{position:relative;background:radial-gradient(120% 90% at 50% 50%,#12264A 0%,var(--bk-navy) 45%,var(--bk-edge) 100%);color:var(--bk-ink);padding:96px 24px;overflow:hidden}
.bk-blurb::after{content:"";position:absolute;left:50%;top:50%;width:900px;height:600px;transform:translate(-50%,-50%);pointer-events:none;background:radial-gradient(circle at center,rgba(255,226,168,.14) 0%,rgba(233,199,126,.08) 22%,transparent 62%);filter:blur(12px)}
.bk-blurb .bk-wrap{max-width:820px;text-align:center}
.bk-blurb .rule{display:block;width:130px;height:1px;background:rgba(233,199,126,.5);margin:0 auto}
.bk-blurb p{font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;font-style:italic;font-weight:500;font-size:clamp(1.75rem,3.4vw,2.7rem);line-height:1.38;color:var(--bk-ink);margin:44px 0;text-wrap:pretty}
/* ---- why ---- */
.bk-excerpt{background:radial-gradient(120% 120% at 15% 10%,#12264A 0%,var(--bk-navy) 55%,var(--bk-edge) 100%);color:var(--bk-ink);border-radius:26px;padding:36px 40px;max-width:860px;margin:0 auto 26px;position:relative;overflow:hidden}
.bk-excerpt::after{content:"";position:absolute;right:-80px;bottom:-140px;width:380px;height:380px;background:radial-gradient(circle,rgba(233,199,126,.26),transparent 65%);filter:blur(8px);pointer-events:none}
.bk-excerpt .lbl{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--bk-gold);margin:0 0 14px;position:relative;z-index:1}
.bk-excerpt p{position:relative;z-index:1;font-size:17.5px;line-height:1.65;margin:0 0 12px;color:#DCE4F1;text-wrap:pretty}
.bk-excerpt p.big{font-size:clamp(1.2rem,2vw,1.5rem);line-height:1.4;font-weight:700;color:#fff;margin:6px 0 0;font-style:italic}
.bk-conv .n{width:32px;height:32px;border-radius:50%;background:#FBF3DF;color:#7A5A1E;font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;margin:0 0 14px;border:1px solid #F0DFB0}
/* ---- inside ---- */
.bk-part .k{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#9A7423;margin:0 0 10px}
.bk-part .t{font-size:19px}
.bk-extras{font-size:14px;color:#8A94A8;text-align:center;margin:18px auto 0;max-width:640px}
/* ---- close ---- */
.bk-close{position:relative;background:radial-gradient(120% 90% at 50% 40%,#12264A 0%,var(--bk-navy) 45%,var(--bk-edge) 100%);color:var(--bk-ink);padding:88px 24px;overflow:hidden}
.bk-close::after{content:"";position:absolute;left:50%;top:70%;width:900px;height:600px;transform:translate(-50%,-50%);pointer-events:none;background:radial-gradient(circle at center,rgba(255,226,168,.2) 0%,rgba(233,199,126,.12) 20%,transparent 62%);filter:blur(12px)}
.bk-close .bk-wrap{display:grid;grid-template-columns:.8fr 1.2fr;gap:56px;align-items:center;max-width:960px}
.bk-close .bk-cover img{max-width:300px}
.bk-close .who{display:flex;flex-direction:column;gap:9px;margin:0 0 28px}
.bk-close .who .lbl{width:100%;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8FA1C0;margin:0 0 4px}
.bk-close .who span.c{font-size:15.5px;font-weight:600;color:#DCE4F1;display:flex;gap:10px;align-items:flex-start;line-height:1.4;text-wrap:pretty}
.bk-close .who span.c::before{content:"";flex-shrink:0;width:6px;height:6px;border-radius:50%;background:var(--bk-gold);margin-top:8px}
.bk-close h2{color:#fff;font-size:clamp(1.7rem,3vw,2.4rem);margin:0 0 10px}
.bk-close .p{font-size:16px;color:#B9C6DC;margin:0 0 24px}
.bk-close .bk-more{color:var(--bk-gold);font-weight:700;font-size:14.5px;text-decoration:none;border-bottom:1px solid rgba(233,199,126,.4);margin-left:6px}
.bk-close .bk-more:hover{border-bottom-color:var(--bk-gold)}
/* ---- author (estilo bigbangbaby.net) ---- */
.bk-author{position:relative;background:radial-gradient(120% 90% at 50% 40%,#12264A 0%,var(--bk-navy) 45%,var(--bk-edge) 100%);color:var(--bk-ink);padding:88px 24px 72px;overflow:hidden}
.bk-author .bk-wrap{max-width:900px;padding-bottom:64px;border-bottom:1px solid rgba(233,199,126,.35)}
.bk-author h2{font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;font-weight:500;font-size:clamp(2.1rem,4vw,3rem);letter-spacing:0;color:#fff;margin:0 0 34px;line-height:1.1}
.bk-author .row{display:grid;grid-template-columns:300px 1fr;gap:40px;align-items:start}
.bk-author img{width:100%;max-width:300px;height:auto;border-radius:6px;display:block;box-shadow:0 30px 60px -30px rgba(0,0,0,.7)}
.bk-author p{font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;font-size:clamp(1.15rem,1.6vw,1.35rem);line-height:1.6;color:var(--bk-ink);margin:0;text-wrap:pretty}
.bk-author a.lnk{display:inline-block;margin-top:26px;color:var(--bk-gold);font-weight:700;text-decoration:none;font-size:15px;border-bottom:1px solid rgba(233,199,126,.4)}
.bk-author a.lnk:hover{border-bottom-color:var(--bk-gold)}
.bk-close{padding-top:72px}
@media(max-width:900px){
  .bk-hero{padding:130px 20px 56px}
  .bk-hero .bk-wrap{grid-template-columns:1fr;gap:32px}
  .bk-hero .bk-cover{order:-1}
  .bk-cover img{max-width:220px}
  .bk-hero h1{font-size:clamp(2.3rem,10vw,3rem)}
  .bk-ctas .bk-btn{width:100%}
  .bk-date{margin:12px 0 0;display:flex}
  .bk-stats{gap:18px}
  .bk-stat .n{font-size:24px}
  .bk-sec{padding:56px 20px}
  .bk-head{margin-bottom:26px}
  .bk-3{grid-template-columns:1fr;gap:12px}
  .bk-card{padding:20px}
  .bk-viz{height:96px}
  .bk-excerpt{padding:26px 22px}
      .bk-blurb{padding:64px 20px}
  .bk-blurb p{margin:32px 0}
  .bk-close{padding:56px 20px}
  .bk-close .bk-wrap{grid-template-columns:1fr;gap:28px;text-align:center;justify-items:center}
  .bk-close .bk-cover img{max-width:200px}
  .bk-close .who{align-items:flex-start;text-align:left}
  .bk-close .bk-ctas{justify-content:center}
  .bk-close .bk-more{margin:4px 0 0}
  .bk-author{padding:56px 20px 40px}
  .bk-author .bk-wrap{padding-bottom:40px}
  .bk-author .row{grid-template-columns:1fr;gap:22px}
  .bk-author img{max-width:240px}
}
"""

LAUNCH_JS = """<script>(function(){if(Date.now()<Date.parse('2026-09-23T06:00:00Z'))return;document.querySelectorAll('[data-after]').forEach(function(e){e.textContent=e.getAttribute('data-after')});})();</script>"""

E = html.escape

def build(lang):
    c = C[lang]
    src = (ROOT / c["src"]).read_text(encoding="utf-8")
    head = re.search(r"<head>(.*?)</head>", src, re.S).group(1)
    tracking = head[: head.find('<meta charset="UTF-8">')].strip()
    nav = re.search(r'<nav class="navbar" id="navbar">.*?</nav>', src, re.S).group(0)
    footer = re.search(r"<footer class=\"footer\">.*?</footer>", src, re.S).group(0)
    tail = src[src.rfind("</footer>") + len("</footer>"):]
    tail = tail[: tail.rfind("</body>")]
    base = c["base"]
    # nav: Science deja de estar activo; el link "Book" queda activo
    nav = nav.replace('<button class="nav-dropdown-toggle active" aria-expanded="false" aria-haspopup="true"><span data-i18n="nav.science">', '<button class="nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true"><span data-i18n="nav.science">', 1)
    nav = nav.replace(f'href="{base}/science" class="nd-item is-active"', f'href="{base}/science" class="nd-item"')
    m = re.search(rf'<a href="{re.escape(base)}/book" data-i18n="nav.book" data-i18n-href="nav.bookUrl"(?: class="active")?>[^<]*</a>', nav)
    assert m, "falta el link Book en el nav fuente"
    nav = nav.replace(m.group(0), m.group(0).replace(' class="active"', '').replace('data-i18n-href="nav.bookUrl">', 'data-i18n-href="nav.bookUrl" class="active">'))

    og = "/og-book.png" if lang == "en" else f"/og-book-{lang}.png"
    url = SITE + c["path"]
    ld = {"@context": "https://schema.org", "@type": "Book", "name": "Big Bang Baby",
          "alternateName": "Big Bang Baby: The Science of How Your Child’s Universe Takes Shape",
          "author": {"@type": "Person", "name": "Luis Garza Sada", "url": SITE + "/founder"},
          "publisher": {"@type": "Organization", "name": "Garza Jasso Press"},
          "isbn": "979-8-9967408-1-9", "bookFormat": "https://schema.org/EBook", "datePublished": "2026-09-23", "inLanguage": "en",
          "image": SITE + "/images/book/cover.webp", "url": url, "sameAs": ["https://bigbangbaby.net/", AMAZON],
          "offers": {"@type": "Offer", "price": "9.99", "priceCurrency": "USD", "url": AMAZON, "availability": "https://schema.org/PreOrder"}}
    lang_attr = {"en": "en", "es": "es", "pt": "pt-BR"}[lang]
    cta_primary = f'<a class="bk-btn bk-btn-gold" href="{AMAZON}" target="_blank" rel="noopener" data-after="{E(c["cta_after"])}">{E(c["cta"])}</a>'
    date_pill = f'<span class="bk-date" data-after="{E(c["date_after"])}">{E(c["date"])}</span>'
    stats = "".join(f'<div class="bk-stat"><div class="n">{E(n)}</div><div class="l">{E(l)}</div></div>' for n, l in c["stats"])
    viz = ['<div class="bk-viz v1"><i class="c"></i></div>',
           '<div class="bk-viz v2"><i class="r r3"></i><i class="r r2"></i><i class="r r1"></i><i class="c"></i></div>',
           '<div class="bk-viz v3"><i class="g"></i><i class="a"></i><i class="b"></i><i class="c3"></i><i class="d"></i></div>']
    idea = "".join(f'<div class="bk-card">{viz[i]}<p class="t"{" lang=\"en\"" if t == Q_BEGIN else ""}>{E(t)}</p><p>{E(p)}</p></div>' for i, (t, p) in enumerate(c["idea"]))
    conv = "".join(f'<div class="bk-card bk-conv"><div class="n">{i+1}</div><p class="t">{E(t)}</p><p>{E(p)}</p></div>' for i, (t, p) in enumerate(c["conv"]))
    parts = "".join(f'<div class="bk-card bk-part"><p class="k">{E(c["part_lbl"][i])}</p><p class="t" lang="en">{E(t)}</p><p>{E(p)}</p></div>' for i, (t, p) in enumerate(c["parts"]))
    who = "".join(f'<span class="c">{E(w)}</span>' for w in c["who"])
    en_note = f' {E(c["en_note"])}' if c["en_note"] else ""

    page = f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="utf-8">
{tracking}
    <meta name="apple-itunes-app" content="app-id=741277284">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{E(c["title"])}</title>
<meta name="description" content="{E(c["desc"])}">
    <link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}/book">
<link rel="alternate" hreflang="es" href="{SITE}/es/book">
<link rel="alternate" hreflang="pt" href="{SITE}/pt/book">
<link rel="alternate" hreflang="x-default" href="{SITE}/book">
<meta property="og:title" content="{E(c["og_title"])}">
<meta property="og:description" content="{E(c["desc"])}">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta property="og:type" content="book">
<meta property="og:site_name" content="Kinedu">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(c["og_title"])}">
<meta name="twitter:description" content="{E(c["desc"])}">
<meta name="twitter:image" content="{SITE}{og}">
    <link rel="preload" href="/fonts/proxima-nova/proximanova-regular-webfont.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonts/proxima-nova/proximanova-bold-webfont.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/images/book/cover-3d.webp" as="image" type="image/webp">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap">
    <link rel="stylesheet" href="/styles.css?v=0842a">
    <link rel="icon" href="/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{nav}
<main class="bk">
<section class="bk-hero bk-stars">
  <div class="bk-wrap">
    <div>
      <span class="bk-kick"><i></i>{E(c["kick"])}</span>
      <h1>Big Bang Baby</h1>
      <p class="bk-subtitle" lang="en">The Science of How Your Child’s Universe Takes Shape</p>
      <p class="bk-by">{E(c["by"])}</p>
      <p class="bk-tag" lang="en">{E(Q_TAG)}</p>
      <p class="bk-lead">{E(c["lead"])}</p>
      <div class="bk-ctas">
        {cta_primary}
        <a class="bk-btn bk-btn-ghost" href="#inside">{E(c["cta2"])}</a>
        {date_pill}
      </div>
      <p class="bk-fine bk-fine-solo">{E(c["fine"])}</p>
    </div>
    <div class="bk-cover">
      <img src="/images/book/cover-3d.webp" srcset="/images/book/cover-3d-sm.webp 420w, /images/book/cover-3d.webp 724w" sizes="(max-width: 900px) 220px, 400px" width="724" height="1179" alt="{E(c["cover_alt"])}" fetchpriority="high">
    </div>
  </div>
</section>

<section class="bk-sec greige" id="idea">
  <div class="bk-wrap">
    <div class="bk-head">
      <span class="bk-kick"><i></i>{E(c["idea_kick"])}</span>
      <h2>{c["idea_h2"]}</h2>
      <p class="bk-lead">{E(c["idea_lead"])}</p>
    </div>
    <div class="bk-3">{idea}</div>
    <p class="bk-note">{E(c["idea_note"])}</p>
  </div>
</section>

<section class="bk-blurb bk-stars">
  <div class="bk-wrap"><span class="rule"></span><p lang="en">{E(BLURB)}</p><span class="rule"></span></div>
</section>

<section class="bk-sec white" id="why">
  <div class="bk-wrap">
    <div class="bk-head">
      <span class="bk-kick"><i></i>{E(c["why_kick"])}</span>
      <h2>{c["why_h2"]}</h2>
      <p class="bk-lead">{E(c["why_lead"])}</p>
    </div>
    <div class="bk-excerpt" lang="en">
      <p class="lbl">{E(c["excerpt_lbl"])}</p>
      <p>{E(EXCERPT)}</p>
      <p class="big">{E(EXCERPT2)}</p>
    </div>
    <div class="bk-3">{conv}</div>
  </div>
</section>

<section class="bk-sec greige" id="inside">
  <div class="bk-wrap">
    <div class="bk-head">
      <span class="bk-kick"><i></i>{E(c["inside_kick"])}</span>
      <h2>{c["inside_h2"]}</h2>
      <p class="bk-lead">{E(c["inside_lead"])}{en_note}</p>
    </div>
    <div class="bk-3">{parts}</div>
    <p class="bk-extras">{E(c["extras"])}</p>
  </div>
</section>

<section class="bk-author bk-stars">
  <div class="bk-wrap">
    <h2>{E(c["auth_kick"])}</h2>
    <div class="row">
      <img src="/images/book/luis-garza-sada-portrait.webp" width="640" height="959" alt="{E(c["photo_alt"])}" loading="lazy">
      <p lang="en">{E(BIO)}</p>
    </div>
    <a class="lnk" href="/founder">{E(c["auth_link"])} →</a>
  </div>
</section>
<section class="bk-close bk-stars">
  <div class="bk-wrap">
    <div class="bk-cover"><img src="/images/book/cover-3d-sm.webp" width="420" height="684" alt="" loading="lazy"></div>
    <div>
      <div class="who"><span class="lbl">{E(c["who_lbl"])}</span>{who}</div>
      <h2 lang="en">{E(c["close_h2"])}</h2>
      <p class="p">{E(c["close_p"])}</p>
      <div class="bk-ctas">
        {cta_primary}
        <a class="bk-more" href="https://bigbangbaby.net/" target="_blank" rel="noopener">{E(c["end_link"])}</a>
      </div>
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

#!/usr/bin/env python3
"""Genera la landing del libro Big Bang Baby (/book, /es/book, /pt/book) y la página
de extracto (/book/introduction y variantes), a partir del nav/footer/scripts de
{lang}/science.html para que header y footer sean los del sitio.

Estructura (reestructura del 15-sep, revisor externo vía Regina): 1) entrada con
pregunta + botones, portada chica; 2) las preguntas detrás de los momentos de todos
los días; 3) un universo tomando forma (un solo visual); 4) empieza con un plátano
roto (extracto real + link a la introducción completa); 5) índice editorial de las
3 partes; 6) autor breve + cierre de compra.

Las frases del libro y el extracto van textuales en inglés (idioma del libro).
Uso:  python3 scripts/book/build.py
"""
import re, html, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
AMAZON = "https://www.amazon.com/dp/B0HHL292P6"
SITE = "https://www.kinedu.com"
E = html.escape

# Textos del libro / sitio del libro, textuales. No se traducen.
BLURB = "Big Bang Baby restores awe and confidence to parenting: your child is not a checklist to complete, but a universe taking shape — and your loving, imperfect presence is one of the forces that helps hold it together."
EXCERPT = [
 "But reality for any parent looks very different. It looks like a father sitting on the kitchen floor at 7:15 in the morning, trying to make the school carpool on time while running late for work, “holding space” for a three-year-old who is screaming because her banana broke in half. The father knows, somewhere deep in the rational part of his brain, that this is developmentally normal. He has read the posts. He understands that a three-year-old does not yet have the capacity to regulate an intense emotional response. He is trying to do the right thing.",
 "The right thing, as described by the parenting internet, involves narrating the child’s emotions back to her (“I see that you’re feeling frustrated about the banana”), validating the experience (“It’s okay to feel sad when something breaks”), and waiting for the storm to pass without any further guidance on emotional regulation or any adult authority that would get the morning back on track.",
 "Meanwhile, three other children need breakfast, school starts in twenty minutes, and the broken banana is now on the floor.",
]
PRE = (HERE / "before-we-begin.html").read_text(encoding="utf-8")
INTRO = (HERE / "introduction.html").read_text(encoding="utf-8")

C = {
 "en": dict(
  path="/book", src="science.html", base="",
  title="Big Bang Baby, the book by Kinedu’s founder | Kinedu",
  desc="How do your child’s skills develop, and what can you do to support them? Big Bang Baby, by Kinedu founder Luis Garza Sada. Read an excerpt and pre-order the book.",
  og_title="Big Bang Baby: the book by Kinedu’s founder",
  kick="The book by Kinedu’s founder",
  date="Kindle edition · In English · Out 23 September 2026", date_after="Kindle edition · In English · Out now",
  q="How do your child’s skills develop, and what can you do to support them?",
  p="In Big Bang Baby, Kinedu founder and father of four Luis Garza Sada explores how early skills connect, why children develop at different paces, and how play, relationships, and everyday routines help them learn.",
  cta="Pre-order on Amazon", cta_after="Get it on Amazon", cta2="Read an excerpt",
  qs_h2="The questions behind the everyday moments.",
  qs=[("Why does one new skill seem to unlock others?", "How movement, language, thinking, and emotions develop together."),
      ("Why do children reach milestones at different times?", "Why the timing varies, and what milestones can and can’t tell you about your child."),
      ("How can you help without turning every moment into a lesson?", "The role of play, warm relationships, clear limits, and familiar routines.")],
  uni_h2="A universe taking shape.",
  uni_p="Early skills are closely connected. As children grow, those skills become more distinct. Big Bang Baby uses the expanding universe as a metaphor for understanding that change.",
  uni_lbl=["Closely connected", "Expanding", "Taking shape"],
  uni_line="A new way to understand the child in front of you.",
  ban_kick="A taste of the book",
  ban_h2="Start with a broken banana.",
  ban_note="From the introduction of Big Bang Baby.",
  ban_link="Read the introduction", ban_more="Read more",
  in_h2="What you’ll find inside.",
  parts=[("The Old Cosmology", "How familiar ideas about child development shaped the advice parents hear today."),
         ("The Big Bang", "How early abilities connect and begin to develop during the first year."),
         ("The Universe Takes Shape", "How children’s skills become more distinct, and how everyday experiences support their development.")],
  part_lbl="Part",
  au_role="Founder of Kinedu. Father of four.",
  au_p="Luis brings his experience building Kinedu and raising four daughters to the questions at the heart of Big Bang Baby: how children develop, and how parents can support them. For more than sixteen years he has worked with early-childhood researchers and educators, and read the questions parents send in at two in the morning. The book sits at that intersection: the science of the first years, and the everyday reality of raising small children.",
  au_link="Meet the author",
  get_h2="Get your copy of Big Bang Baby.",
  get_details=["Kindle edition, $9.99 USD", "In English", "23 September 2026", "Paperback coming soon"],
  get_more="bigbangbaby.net",
  cover_alt="Big Bang Baby, the book by Luis Garza Sada",
  photo_alt="Luis Garza Sada, author of Big Bang Baby and founder of Kinedu",
  ix_path="/book/introduction",
  ix_title="Big Bang Baby: read the introduction | Kinedu",
  ix_desc="The full introduction of Big Bang Baby, the book by Kinedu founder Luis Garza Sada.",
  ix_kick="From the book", ix_back="Back to the book", ix_note="Reproduced from Big Bang Baby. About 15 minutes.",
  ix_end_h="The introduction ends here.", ix_end_p="The rest is in the book.",
 ),
 "es": dict(
  path="/es/book", src="es/science.html", base="/es",
  title="Big Bang Baby, el libro del fundador de Kinedu | Kinedu",
  desc="¿Cómo se desarrollan las habilidades de tu hijo y qué puedes hacer para apoyarlas? Big Bang Baby, de Luis Garza Sada, fundador de Kinedu. Lee un extracto y reserva el libro.",
  og_title="Big Bang Baby: el libro del fundador de Kinedu",
  kick="El libro del fundador de Kinedu",
  date="Edición Kindle · En inglés · Sale el 23 de septiembre de 2026", date_after="Edición Kindle · En inglés · Ya disponible",
  q="¿Cómo se desarrollan las habilidades de tu hijo y qué puedes hacer para apoyarlas?",
  p="En Big Bang Baby, Luis Garza Sada, fundador de Kinedu y papá de cuatro, explora cómo se conectan las primeras habilidades, por qué cada niño se desarrolla a su ritmo y cómo el juego, las relaciones y las rutinas de todos los días los ayudan a aprender.",
  cta="Reserva en Amazon", cta_after="Cómpralo en Amazon", cta2="Lee un extracto",
  qs_h2="Las preguntas detrás de los momentos de todos los días.",
  qs=[("¿Por qué una habilidad nueva parece desbloquear otras?", "Cómo el movimiento, el lenguaje, el pensamiento y las emociones se desarrollan juntos."),
      ("¿Por qué los niños alcanzan los hitos en momentos distintos?", "Por qué varían los tiempos, y qué pueden y qué no pueden decirte los hitos sobre tu hijo."),
      ("¿Cómo ayudar sin convertir cada momento en una lección?", "El papel del juego, las relaciones cálidas, los límites claros y las rutinas conocidas.")],
  uni_h2="Un universo tomando forma.",
  uni_p="Las primeras habilidades están muy conectadas. Conforme los niños crecen, esas habilidades se vuelven más distintas. Big Bang Baby usa el universo en expansión como metáfora para entender ese cambio.",
  uni_lbl=["Muy conectadas", "En expansión", "Tomando forma"],
  uni_line="Una nueva forma de entender al niño que tienes enfrente.",
  ban_kick="Una probada del libro",
  ban_h2="Empieza con un plátano roto.",
  ban_note="De la introducción de Big Bang Baby, en inglés.",
  ban_link="Lee la introducción", ban_more="Leer más",
  in_h2="Qué vas a encontrar dentro.",
  parts=[("The Old Cosmology", "Cómo las ideas conocidas sobre el desarrollo infantil moldearon los consejos que los papás escuchan hoy."),
         ("The Big Bang", "Cómo se conectan las primeras capacidades y empiezan a desarrollarse durante el primer año."),
         ("The Universe Takes Shape", "Cómo las habilidades de los niños se vuelven más distintas y cómo las experiencias cotidianas apoyan su desarrollo.")],
  part_lbl="Parte",
  au_role="Fundador de Kinedu. Papá de cuatro.",
  au_p="Luis lleva su experiencia construyendo Kinedu y criando a cuatro hijas a las preguntas que están en el corazón de Big Bang Baby: cómo se desarrollan los niños y cómo pueden apoyarlos sus papás. Desde hace más de dieciséis años trabaja con investigadores y educadores de primera infancia, y ha leído las preguntas que los papás mandan a las dos de la mañana. El libro vive en ese cruce: la ciencia de los primeros años y la realidad de todos los días de criar niños pequeños.",
  au_link="Conoce al autor",
  get_h2="Consigue tu ejemplar de Big Bang Baby.",
  get_details=["Edición Kindle, 9.99 USD", "En inglés", "23 de septiembre de 2026", "Pasta blanda próximamente"],
  get_more="bigbangbaby.net",
  cover_alt="Big Bang Baby, el libro de Luis Garza Sada",
  photo_alt="Luis Garza Sada, autor de Big Bang Baby y fundador de Kinedu",
  ix_path="/es/book/introduction",
  ix_title="Big Bang Baby: lee la introducción | Kinedu",
  ix_desc="La introducción completa de Big Bang Baby, el libro de Luis Garza Sada, fundador de Kinedu.",
  ix_kick="Del libro", ix_back="Volver al libro", ix_note="Reproducida de Big Bang Baby, en su inglés original. Unos 15 minutos de lectura.",
  ix_end_h="La introducción termina aquí.", ix_end_p="El resto está en el libro.",
 ),
 "pt": dict(
  path="/pt/book", src="pt/science.html", base="/pt",
  title="Big Bang Baby, o livro do fundador do Kinedu | Kinedu",
  desc="Como as habilidades do seu filho se desenvolvem, e o que você pode fazer para apoiá-las? Big Bang Baby, de Luis Garza Sada, fundador do Kinedu. Leia um trecho e reserve o livro.",
  og_title="Big Bang Baby: o livro do fundador do Kinedu",
  kick="O livro do fundador do Kinedu",
  date="Edição Kindle · Em inglês · Lançamento em 23 de setembro de 2026", date_after="Edição Kindle · Em inglês · Já disponível",
  q="Como as habilidades do seu filho se desenvolvem, e o que você pode fazer para apoiá-las?",
  p="Em Big Bang Baby, Luis Garza Sada, fundador do Kinedu e pai de quatro, explora como as primeiras habilidades se conectam, por que cada criança se desenvolve no seu ritmo e como a brincadeira, as relações e as rotinas do dia a dia as ajudam a aprender.",
  cta="Reserve na Amazon", cta_after="Compre na Amazon", cta2="Leia um trecho",
  qs_h2="As perguntas por trás dos momentos do dia a dia.",
  qs=[("Por que uma habilidade nova parece destravar outras?", "Como movimento, linguagem, pensamento e emoções se desenvolvem juntos."),
      ("Por que as crianças alcançam os marcos em momentos diferentes?", "Por que os tempos variam, e o que os marcos podem e não podem dizer sobre o seu filho."),
      ("Como ajudar sem transformar cada momento em uma lição?", "O papel da brincadeira, das relações afetuosas, dos limites claros e das rotinas familiares.")],
  uni_h2="Um universo tomando forma.",
  uni_p="As primeiras habilidades são muito conectadas. À medida que as crianças crescem, essas habilidades se tornam mais distintas. Big Bang Baby usa o universo em expansão como metáfora para entender essa mudança.",
  uni_lbl=["Muito conectadas", "Em expansão", "Tomando forma"],
  uni_line="Um novo jeito de entender a criança que está na sua frente.",
  ban_kick="Um gostinho do livro",
  ban_h2="Comece com uma banana quebrada.",
  ban_note="Da introdução de Big Bang Baby, em inglês.",
  ban_link="Leia a introdução", ban_more="Ler mais",
  in_h2="O que você vai encontrar dentro.",
  parts=[("The Old Cosmology", "Como ideias conhecidas sobre o desenvolvimento infantil moldaram os conselhos que os pais ouvem hoje."),
         ("The Big Bang", "Como as primeiras capacidades se conectam e começam a se desenvolver durante o primeiro ano."),
         ("The Universe Takes Shape", "Como as habilidades das crianças se tornam mais distintas e como as experiências do dia a dia apoiam seu desenvolvimento.")],
  part_lbl="Parte",
  au_role="Fundador do Kinedu. Pai de quatro.",
  au_p="Luis leva sua experiência construindo o Kinedu e criando quatro filhas às perguntas que estão no coração de Big Bang Baby: como as crianças se desenvolvem e como os pais podem apoiá-las. Há mais de dezesseis anos trabalha com pesquisadores e educadores de primeira infância, e já leu as perguntas que os pais mandam às duas da manhã. O livro vive nesse cruzamento: a ciência dos primeiros anos e a realidade do dia a dia de criar crianças pequenas.",
  au_link="Conheça o autor",
  get_h2="Garanta seu exemplar de Big Bang Baby.",
  get_details=["Edição Kindle, US$ 9,99", "Em inglês", "23 de setembro de 2026", "Brochura em breve"],
  get_more="bigbangbaby.net",
  cover_alt="Big Bang Baby, o livro de Luis Garza Sada",
  photo_alt="Luis Garza Sada, autor de Big Bang Baby e fundador do Kinedu",
  ix_path="/pt/book/introduction",
  ix_title="Big Bang Baby: leia a introdução | Kinedu",
  ix_desc="A introdução completa de Big Bang Baby, o livro de Luis Garza Sada, fundador do Kinedu.",
  ix_kick="Do livro", ix_back="Voltar ao livro", ix_note="Reproduzida de Big Bang Baby, no inglês original. Cerca de 15 minutos de leitura.",
  ix_end_h="A introdução termina aqui.", ix_end_p="O resto está no livro.",
 ),
}

CSS = r"""
:root{--bk-navy:#0A1A33;--bk-edge:#050D1F;--bk-ink:#EDF1F8;--bk-gold:#E9C77E;--bk-gold-ink:#2A2009;--bk-text:#1A1D2E;--bk-muted:#52607A}
.bk{font-family:'Proxima Nova','Inter',-apple-system,BlinkMacSystemFont,sans-serif;color:var(--bk-text);overflow-x:hidden}
.bk *{box-sizing:border-box}
.bk-wrap{max-width:1040px;margin:0 auto;position:relative;z-index:1}
.bk-kick{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#7A5A1E;background:#FBF3DF;border:1px solid #F0DFB0;border-radius:999px;padding:7px 14px;margin:0 0 18px}
.bk-kick i{width:6px;height:6px;border-radius:50%;background:var(--bk-gold);display:inline-block}
.bk h2{font-size:clamp(1.8rem,3.2vw,2.5rem);line-height:1.12;letter-spacing:-.025em;font-weight:800;color:#081B46;margin:0 0 16px;text-wrap:balance}
.bk-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:999px;padding:16px 30px;font-weight:800;font-size:15.5px;text-decoration:none;transition:transform .15s,box-shadow .15s,background .15s;white-space:nowrap}
.bk-btn:hover{transform:translateY(-2px)}
.bk-btn-gold{background:var(--bk-gold);color:var(--bk-gold-ink);box-shadow:0 18px 40px -16px rgba(233,199,126,.7)}
.bk-btn-gold:hover{background:#F2D48E}
.bk-btn-ghost{background:transparent;color:var(--bk-ink);border:1.5px solid rgba(237,241,248,.45)}
.bk-btn-ghost:hover{border-color:rgba(237,241,248,.9)}
.bk-ctas{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.bk-date{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--bk-gold);margin-left:10px}
.bk-date::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--bk-gold)}
.bk-navy{position:relative;background:radial-gradient(120% 90% at 50% 45%,#12264A 0%,var(--bk-navy) 45%,var(--bk-edge) 100%);color:var(--bk-ink);overflow:hidden}
.bk-stars::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(1.4px 1.4px at 8% 22%,rgba(157,180,214,.9),transparent 60%),radial-gradient(1px 1px at 18% 68%,rgba(157,180,214,.7),transparent 60%),radial-gradient(1.6px 1.6px at 27% 38%,rgba(255,255,255,.75),transparent 60%),radial-gradient(1px 1px at 36% 82%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.2px 1.2px at 44% 14%,rgba(157,180,214,.8),transparent 60%),radial-gradient(1px 1px at 57% 58%,rgba(157,180,214,.55),transparent 60%),radial-gradient(1.8px 1.8px at 66% 24%,rgba(255,255,255,.7),transparent 60%),radial-gradient(1px 1px at 73% 76%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.3px 1.3px at 84% 40%,rgba(157,180,214,.85),transparent 60%),radial-gradient(1px 1px at 92% 66%,rgba(157,180,214,.6),transparent 60%),radial-gradient(1.5px 1.5px at 12% 90%,rgba(255,255,255,.55),transparent 60%),radial-gradient(1px 1px at 61% 92%,rgba(157,180,214,.5),transparent 60%),radial-gradient(1.2px 1.2px at 96% 12%,rgba(157,180,214,.7),transparent 60%)}
.bk-panel{border-radius:30px;padding:60px 60px;max-width:1160px;margin:0 auto;box-shadow:0 30px 70px -40px rgba(8,27,70,.45)}
/* 1. entrada */
.bk-hero{background:#FBFAF8;padding:130px 24px 36px}
.bk-hero .bk-panel::after{content:"";position:absolute;left:66%;top:58%;width:760px;height:600px;transform:translate(-50%,-50%);pointer-events:none;background:radial-gradient(circle at center,rgba(255,226,168,.2) 0%,rgba(233,199,126,.13) 18%,rgba(214,168,92,.05) 42%,transparent 66%);filter:blur(10px)}
.bk-hero .bk-wrap{display:grid;grid-template-columns:1.25fr .75fr;gap:48px;align-items:center}
.bk-hero .bk-kick{color:var(--bk-gold);background:rgba(233,199,126,.08);border-color:rgba(233,199,126,.28)}
.bk-hero h1{font-size:clamp(2.4rem,5.2vw,4rem);line-height:.98;letter-spacing:.04em;text-transform:uppercase;font-weight:800;color:#fff;margin:0 0 12px}
.bk-hero .bk-subtitle{font-size:clamp(1.05rem,1.7vw,1.3rem);line-height:1.35;color:#C9D3E6;margin:0 0 28px;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
.bk-hero .bk-q{font-size:clamp(1.3rem,2.1vw,1.7rem);line-height:1.25;font-weight:800;color:#fff;margin:0 0 14px;letter-spacing:-.02em;text-wrap:balance}
.bk-hero .bk-p{font-size:clamp(1rem,1.4vw,1.15rem);line-height:1.6;color:#C9D3E6;margin:0 0 28px;max-width:600px;text-wrap:pretty}
.bk-cover{position:relative;display:flex;justify-content:center}
.bk-cover img{width:100%;max-width:320px;height:auto;display:block;filter:drop-shadow(0 40px 60px rgba(0,0,0,.55))}
/* 2. preguntas */
.bk-qs{background:#FBFAF8;padding:80px 24px}
.bk-qs h2{max-width:640px;margin:0 0 36px}
.bk-qs .row{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
.bk-qs .it{border-top:2px solid #E9C77E;padding-top:20px}
.bk-qs .it .q{font-size:19px;font-weight:800;color:#081B46;line-height:1.3;margin:0 0 10px;letter-spacing:-.01em;text-wrap:balance}
.bk-qs .it p{font-size:15.5px;line-height:1.58;color:var(--bk-muted);margin:0;text-wrap:pretty}
/* 3. universo */
.bk-uni{padding:84px 24px}
.bk-uni .bk-wrap{display:grid;grid-template-columns:.9fr 1.1fr;gap:48px;align-items:center}
.bk-uni h2{color:#fff}
.bk-uni .p{font-size:clamp(1rem,1.4vw,1.15rem);line-height:1.6;color:#C9D3E6;margin:0;text-wrap:pretty}
.bk-uni svg{width:100%;height:auto;display:block}
.bk-uni .lbls{display:grid;grid-template-columns:repeat(3,1fr);text-align:center;margin-top:8px}
.bk-uni .lbls span{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8FA1C0}
.bk-uni .blurb{grid-column:1/-1;margin:36px auto 0;max-width:760px;text-align:center;font-weight:800;font-size:clamp(1.3rem,2.2vw,1.7rem);line-height:1.3;letter-spacing:-.02em;color:#fff;padding-top:30px;border-top:1px solid rgba(233,199,126,.35);text-wrap:balance}
/* 4. plátano */
.bk-ban{background:#fff;padding:84px 24px;border-top:1px solid #F0EDE7}
.bk-ban .bk-wrap{max-width:720px}
.bk-ban .note{font-size:13.5px;color:#8A94A8;margin:0 0 26px}
.bk-ban .ex{font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;font-size:clamp(1.25rem,1.9vw,1.5rem);line-height:1.55;color:#1A1D2E;border-left:2px solid #E9C77E;padding-left:26px;margin:0 0 28px}
.bk-ban .ex p{margin:0 0 1em;text-wrap:pretty}
.bk-ban .ex p:last-child{margin:0;font-weight:600}
.bk-ban .ex p.rest{display:none}
.bk-ban .ex.open p.rest{display:block}
.bk-btn-navy{background:#081B46;color:#fff;box-shadow:0 18px 40px -16px rgba(8,27,70,.6)}
.bk-btn-navy:hover{background:#12264A}
.bk-ban .bk-readmore{margin:0 0 6px}
.bk-ban a.more{color:#081B46;font-weight:800;text-decoration:none;font-size:16px;border-bottom:2px solid #E9C77E;padding-bottom:2px}
.bk-ban a.more:hover{border-bottom-color:#081B46}
/* 5. índice */
.bk-in{background:#FBFAF8;padding:80px 24px}
.bk-in h2{margin-bottom:28px}
.bk-in .toc{max-width:860px}
.bk-in .rw{display:grid;grid-template-columns:92px 1fr;gap:24px;align-items:baseline;padding:26px 0;border-top:1px solid #E4DED4}
.bk-in .rw:last-child{border-bottom:1px solid #E4DED4}
.bk-in .rw .n{font-size:46px;font-weight:800;letter-spacing:-.04em;color:#C9A44A;line-height:1}
.bk-in .rw .n small{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8A94A8;margin-top:6px;font-weight:800}
.bk-in .rw .t{font-size:21px;font-weight:800;color:#081B46;margin:0 0 6px;letter-spacing:-.01em}
.bk-in .rw p{font-size:15.5px;line-height:1.58;color:var(--bk-muted);margin:0;max-width:600px;text-wrap:pretty}
/* 6. autor + cierre */
.bk-end{background:#FBFAF8;padding:36px 24px 88px}
.bk-end .bk-panel::after{content:"";position:absolute;left:50%;top:78%;width:900px;height:600px;transform:translate(-50%,-50%);pointer-events:none;background:radial-gradient(circle at center,rgba(255,226,168,.18) 0%,rgba(233,199,126,.1) 20%,transparent 62%);filter:blur(12px)}
.bk-end .bk-wrap{max-width:900px}
.bk-au{display:grid;grid-template-columns:120px 1fr;gap:30px;align-items:center;padding-bottom:48px;border-bottom:1px solid rgba(233,199,126,.3);margin-bottom:48px}
.bk-au img{width:120px;height:120px;border-radius:50%;object-fit:cover;display:block;box-shadow:0 20px 40px -20px rgba(0,0,0,.7)}
.bk-au .nm{font-size:1.35rem;font-weight:800;color:#fff;margin:0 0 4px;letter-spacing:-.01em}
.bk-au .rl{font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--bk-gold);margin:0 0 10px}
.bk-au p{font-size:16px;line-height:1.6;color:#C9D3E6;margin:0 0 10px;text-wrap:pretty}
.bk-au a{color:var(--bk-gold);font-weight:700;text-decoration:none;font-size:14.5px;border-bottom:1px solid rgba(233,199,126,.4)}
.bk-au a:hover{border-bottom-color:var(--bk-gold)}
.bk-get{display:grid;grid-template-columns:150px 1fr;gap:36px;align-items:center}
.bk-get img{width:150px;height:auto;display:block;filter:drop-shadow(0 24px 34px rgba(0,0,0,.55))}
.bk-get h2{color:#fff;margin-bottom:14px}
.bk-get .dt{list-style:none;padding:0;margin:0 0 22px;display:flex;flex-wrap:wrap;gap:6px 18px}
.bk-get .dt li{font-size:14.5px;color:#C9D3E6;font-weight:600;display:flex;align-items:center;gap:8px}
.bk-get .dt li::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--bk-gold)}
.bk-get .more{color:var(--bk-gold);font-weight:700;font-size:14.5px;text-decoration:none;border-bottom:1px solid rgba(233,199,126,.4);margin-left:6px}
.bk-get .more:hover{border-bottom-color:var(--bk-gold)}
/* página de extracto */
.bk-ix{background:#fff;padding:150px 24px 72px}
.bk-ix .bk-head{max-width:680px;margin:0 auto 36px}
.bk-ix .bk-head .back{display:inline-block;font-size:14px;font-weight:700;color:#087BF3;text-decoration:none;margin:0 0 18px}
.bk-ix .bk-head h1{font-size:clamp(1.8rem,3.2vw,2.5rem);line-height:1.12;letter-spacing:-.025em;font-weight:800;color:#081B46;margin:0 0 8px;text-wrap:balance}
.bk-ix .bk-head .sub{font-size:1.05rem;color:#8A94A8;margin:0 0 6px;font-style:italic}
.bk-ix .bk-head .note{font-size:13.5px;color:#8A94A8;margin:0}
.bk-rule{width:56px;height:2px;background:var(--bk-gold);border-radius:2px;margin:0 auto 40px}
.bk-essay{max-width:680px;margin:0 auto;font-size:19px;line-height:1.72;color:var(--bk-text)}
.bk-essay h2{font-size:clamp(1.6rem,2.6vw,2.05rem);line-height:1.15;letter-spacing:-.02em;margin:0 0 8px;color:#081B46;text-wrap:balance}
.bk-essay h2.bk-h-pre{font-size:1.35rem;margin-bottom:6px}
.bk-essay h3{font-size:1.2rem;line-height:1.3;font-weight:800;color:#081B46;margin:52px 0 14px;letter-spacing:-.01em;text-wrap:balance}
.bk-essay p{margin:0 0 1.15em;text-wrap:pretty}
.bk-essay strong{color:#081B46}
.bk-essay .bk-pre{background:#FBFAF8;border:1px solid #EBE6DF;border-radius:20px;padding:28px 30px 12px;margin:0 0 48px;font-size:17px;line-height:1.68}
.bk-ixend{max-width:680px;margin:56px auto 0;border-radius:26px;padding:34px 36px;display:grid;grid-template-columns:96px 1fr;gap:28px;align-items:center}
.bk-ixend img{width:96px;height:auto;display:block;filter:drop-shadow(0 18px 24px rgba(0,0,0,.5));position:relative;z-index:1}
.bk-ixend .t{position:relative;z-index:1}
.bk-ixend .h{font-size:1.35rem;font-weight:800;color:#fff;margin:0 0 4px}
.bk-ixend .p{font-size:1rem;color:#C9D3E6;margin:0 0 18px}
@media(max-width:900px){
  .bk-hero{padding:104px 16px 24px}
  .bk-panel{border-radius:22px;padding:36px 22px}
  .bk-hero .bk-wrap{grid-template-columns:1fr;gap:28px}
  .bk-hero .bk-cover{order:-1}
  .bk-cover img{max-width:200px}
  .bk-hero h1{font-size:clamp(2.2rem,9vw,2.8rem)}
  .bk-ctas .bk-btn{width:100%}
  .bk-date{margin:12px 0 0;display:flex}
  .bk-qs,.bk-uni,.bk-ban,.bk-in{padding:56px 20px}
  .bk-end{padding:24px 16px 56px}
  .bk-qs .row{grid-template-columns:1fr;gap:24px}
  .bk-uni .bk-wrap{grid-template-columns:1fr;gap:28px}
  .bk-uni .blurb{margin-top:28px}
  .bk-ban .ex{padding-left:18px;font-size:1.2rem}
  .bk-in .rw{grid-template-columns:64px 1fr;gap:16px;padding:20px 0}
  .bk-in .rw .n{font-size:34px}
  .bk-au{grid-template-columns:1fr;text-align:center;justify-items:center;gap:16px;padding-bottom:36px;margin-bottom:36px}
  .bk-get{grid-template-columns:1fr;text-align:center;justify-items:center;gap:22px}
  .bk-get .dt{justify-content:center}
  .bk-get .bk-ctas{justify-content:center}
  .bk-ix{padding:120px 20px 56px}
  .bk-essay{font-size:17.5px;line-height:1.7}
  .bk-essay .bk-pre{padding:22px 20px 8px;font-size:16px}
  .bk-ixend{grid-template-columns:1fr;padding:26px 22px;text-align:center;justify-items:center}
  .bk-ixend .bk-ctas{justify-content:center}
}
"""

LAUNCH_JS = """<script>(function(){var b=document.getElementById('bkExMore');if(b){b.addEventListener('click',function(){document.getElementById('bkEx').classList.add('open');b.hidden=true;});}})();</script>
<script>(function(){if(Date.now()<Date.parse('2026-09-23T06:00:00Z'))return;document.querySelectorAll('[data-after]').forEach(function(e){e.textContent=e.getAttribute('data-after')});})();</script>"""

def universe_svg():
    """Un solo visual: conexiones densas → expansión → cuatro áreas distintas."""
    import math
    out = ['<svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true">',
           '<defs><radialGradient id="bkg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FDF6E3" stop-opacity=".95"/><stop offset=".35" stop-color="#E9C77E" stop-opacity=".45"/><stop offset="1" stop-color="#E9C77E" stop-opacity="0"/></radialGradient></defs>']
    out.append('<path d="M150 150 C 300 150, 320 150, 450 150 S 640 150, 750 150" stroke="rgba(233,199,126,.28)" stroke-width="1" fill="none" stroke-dasharray="3 6"/>')
    cx, cy = 150, 150
    pts = [(cx + 34*math.cos(a)*(0.6 + 0.4*((i*7)%3)/2), cy + 34*math.sin(a)*(0.6 + 0.4*((i*5)%3)/2)) for i, a in enumerate([k*math.pi/5 for k in range(10)])]
    out.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="url(#bkg)"/>')
    for i, (x1, y1) in enumerate(pts):
        for j, (x2, y2) in enumerate(pts):
            if j > i and (i + j) % 2 == 0:
                out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="rgba(237,241,248,.35)" stroke-width="1"/>')
    for x, y in pts:
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#FDF6E3"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#FDF6E3"/>')
    cx = 450
    out.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="rgba(233,199,126,.45)"/><circle cx="{cx}" cy="{cy}" r="64" fill="none" stroke="rgba(233,199,126,.25)"/><circle cx="{cx}" cy="{cy}" r="96" fill="none" stroke="rgba(233,199,126,.12)"/>')
    pts2 = [(cx + r*math.cos(a), cy + r*math.sin(a)) for (r, a) in [(34, .3), (34, 2.4), (34, 4.2), (64, 1.1), (64, 3.3), (64, 5.4), (96, .8), (96, 2.9), (96, 4.9)]]
    for x, y in pts2:
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="rgba(237,241,248,.22)" stroke-width="1"/><circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#EDF1F8"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#FDF6E3"/>')
    cx = 750
    cols = ["#2B8BE4", "#4CD964", "#E84D8A", "#FFC033"]
    cents = [(cx - 62, cy - 58), (cx + 62, cy - 58), (cx - 62, cy + 58), (cx + 62, cy + 58)]
    for (x, y), col in zip(cents, cols):
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="rgba(237,241,248,.12)" stroke-width="1"/>')
        for k in range(5):
            a = k * 2 * math.pi / 5 + 0.4
            sx, sy = x + 26*math.cos(a), y + 26*math.sin(a)
            out.append(f'<line x1="{x}" y1="{y}" x2="{sx:.0f}" y2="{sy:.0f}" stroke="{col}" stroke-opacity=".45" stroke-width="1"/><circle cx="{sx:.0f}" cy="{sy:.0f}" r="2.6" fill="{col}"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{col}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="rgba(237,241,248,.5)"/>')
    out.append('</svg>')
    return "".join(out)

def chrome(lang):
    c = C[lang]
    src = (ROOT / c["src"]).read_text(encoding="utf-8")
    head = re.search(r"<head>(.*?)</head>", src, re.S).group(1)
    tracking = head[: head.find('<meta charset="UTF-8">')].strip()
    nav = re.search(r'<nav class="navbar" id="navbar">.*?</nav>', src, re.S).group(0)
    footer = re.search(r"<footer class=\"footer\">.*?</footer>", src, re.S).group(0)
    tail = src[src.rfind("</footer>") + len("</footer>"):]
    tail = tail[: tail.rfind("</body>")].strip()
    base = c["base"]
    nav = nav.replace('<button class="nav-dropdown-toggle active" aria-expanded="false" aria-haspopup="true"><span data-i18n="nav.science">', '<button class="nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true"><span data-i18n="nav.science">', 1)
    nav = nav.replace(f'href="{base}/science" class="nd-item is-active"', f'href="{base}/science" class="nd-item"')
    m = re.search(rf'<a href="{re.escape(base)}/book" data-i18n="nav.book" data-i18n-href="nav.bookUrl"(?: class="active")?>[^<]*</a>', nav)
    assert m, "falta el link Book en el nav fuente"
    nav = nav.replace(m.group(0), m.group(0).replace(' class="active"', '').replace('data-i18n-href="nav.bookUrl">', 'data-i18n-href="nav.bookUrl" class="active">'))
    # rutas absolutas: /book/introduction vive un nivel más abajo
    nav = nav.replace('src="logo kinedu.png"', 'src="/logo kinedu.png"')
    footer = footer.replace('src="logo kinedu.png"', 'src="/logo kinedu.png"')
    tail = tail.replace('src="translations.js?', 'src="/translations.js?').replace('src="script.js?', 'src="/script.js?')
    return tracking, nav, footer, tail

def head_html(lang, title, desc, path, og_title, ld, alt_paths):
    og = "/og-book.png" if lang == "en" else f"/og-book-{lang}.png"
    url = SITE + path
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{p}">\n' for l, p in alt_paths) + f'<link rel="alternate" hreflang="x-default" href="{SITE}{alt_paths[0][1]}">'
    return f"""    <meta name="apple-itunes-app" content="app-id=741277284">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
    <link rel="canonical" href="{url}">
{alts}
<meta property="og:title" content="{E(og_title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta property="og:type" content="book">
<meta property="og:site_name" content="Kinedu">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(og_title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE}{og}">
    <link rel="preload" href="/fonts/proxima-nova/proximanova-regular-webfont.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonts/proxima-nova/proximanova-bold-webfont.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap">
    <link rel="stylesheet" href="/styles.css?v=0842a">
    <link rel="icon" href="/favicon.png" type="image/png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>"""

def book_ld(url):
    return {"@context": "https://schema.org", "@type": "Book", "name": "Big Bang Baby",
            "alternateName": "Big Bang Baby: The Science of How Your Child’s Universe Takes Shape",
            "author": {"@type": "Person", "name": "Luis Garza Sada", "url": SITE + "/founder"},
            "publisher": {"@type": "Organization", "name": "Garza Jasso Press"},
            "isbn": "979-8-9967408-1-9", "bookFormat": "https://schema.org/EBook", "datePublished": "2026-09-23", "inLanguage": "en",
            "image": SITE + "/images/book/cover.webp", "url": url, "sameAs": ["https://bigbangbaby.net/", AMAZON],
            "offers": {"@type": "Offer", "price": "9.99", "priceCurrency": "USD", "url": AMAZON, "availability": "https://schema.org/PreOrder"}}

def page_html(lang, head_inner, body_inner):
    tracking, nav, footer, tail = chrome(lang)
    lang_attr = {"en": "en", "es": "es", "pt": "pt-BR"}[lang]
    return f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="utf-8">
{tracking}
{head_inner}
</head>
<body>
{nav}
<main class="bk">
{body_inner}
</main>
{footer}
{tail}
{LAUNCH_JS}
</body>
</html>
"""

def build_landing(lang):
    c = C[lang]; base = c["base"]
    cta = f'<a class="bk-btn bk-btn-gold" href="{AMAZON}" target="_blank" rel="noopener" data-after="{E(c["cta_after"])}">{E(c["cta"])}</a>'
    date_pill = f'<span class="bk-date" data-after="{E(c["date_after"])}">{E(c["date"])}</span>'
    qs = "".join(f'<div class="it"><p class="q">{E(q)}</p><p>{E(p)}</p></div>' for q, p in c["qs"])
    lbls = "".join(f'<span>{E(l)}</span>' for l in c["uni_lbl"])
    ex = "".join(f'<p{" class=\"rest\"" if i else ""}>{E(p)}</p>' for i, p in enumerate(EXCERPT))
    toc = "".join(f'<div class="rw"><div class="n">{i+1}<small>{E(c["part_lbl"])}</small></div><div><p class="t" lang="en">{E(t)}</p><p>{E(p)}</p></div></div>' for i, (t, p) in enumerate(c["parts"]))
    dts = "".join(f'<li>{E(d)}</li>' for d in c["get_details"])
    body = f"""<section class="bk-hero">
  <div class="bk-panel bk-navy bk-stars">
  <div class="bk-wrap">
    <div>
      <span class="bk-kick"><i></i>{E(c["kick"])}</span>
      <h1>Big Bang Baby</h1>
      <p class="bk-subtitle" lang="en">The Science of How Your Child’s Universe Takes Shape</p>
      <p class="bk-q">{E(c["q"])}</p>
      <p class="bk-p">{E(c["p"])}</p>
      <div class="bk-ctas">
        {cta}
        <a class="bk-btn bk-btn-ghost" href="#excerpt">{E(c["cta2"])}</a>
        {date_pill}
      </div>
    </div>
    <div class="bk-cover">
      <img src="/images/book/cover-3d.webp" srcset="/images/book/cover-3d-sm.webp 420w, /images/book/cover-3d.webp 724w" sizes="(max-width: 900px) 200px, 320px" width="724" height="1179" alt="{E(c["cover_alt"])}" fetchpriority="high">
    </div>
  </div>
  </div>
</section>

<section class="bk-qs" id="questions">
  <div class="bk-wrap">
    <h2>{E(c["qs_h2"])}</h2>
    <div class="row">{qs}</div>
  </div>
</section>

<section class="bk-uni bk-navy bk-stars" id="universe">
  <div class="bk-wrap">
    <div>
      <h2>{E(c["uni_h2"])}</h2>
      <p class="p">{E(c["uni_p"])}</p>
    </div>
    <div>
      {universe_svg()}
      <div class="lbls">{lbls}</div>
    </div>
    <p class="blurb">{E(c["uni_line"])}</p>
  </div>
</section>

<section class="bk-ban" id="excerpt">
  <div class="bk-wrap">
    <span class="bk-kick"><i></i>{E(c["ban_kick"])}</span>
    <h2>{E(c["ban_h2"])}</h2>
    <p class="note">{E(c["ban_note"])}</p>
    <div class="ex" lang="en" id="bkEx">{ex}</div>
    <button type="button" class="bk-btn bk-btn-navy bk-readmore" id="bkExMore">{E(c["ban_more"])}</button>
  </div>
</section>

<section class="bk-in" id="inside">
  <div class="bk-wrap">
    <h2>{E(c["in_h2"])}</h2>
    <div class="toc">{toc}</div>
  </div>
</section>

<section class="bk-end" id="get">
  <div class="bk-panel bk-navy bk-stars">
  <div class="bk-wrap">
    <div class="bk-au">
      <img src="/images/book/luis-garza-sada.webp" width="120" height="120" alt="{E(c["photo_alt"])}" loading="lazy">
      <div>
        <p class="nm">Luis Garza Sada</p>
        <p class="rl">{E(c["au_role"])}</p>
        <p>{E(c["au_p"])}</p>
        <a href="/founder">{E(c["au_link"])} →</a>
      </div>
    </div>
    <div class="bk-get">
      <img src="/images/book/cover-3d-sm.webp" width="420" height="684" alt="" loading="lazy">
      <div>
        <h2>{E(c["get_h2"])}</h2>
        <ul class="dt">{dts}</ul>
        <div class="bk-ctas">{cta}<a class="more" href="https://bigbangbaby.net/" target="_blank" rel="noopener">{E(c["get_more"])}</a></div>
      </div>
    </div>
  </div>
  </div>
</section>"""
    head = head_html(lang, c["title"], c["desc"], c["path"], c["og_title"], book_ld(SITE + c["path"]), [("en", "/book"), ("es", "/es/book"), ("pt", "/pt/book")])
    out = ROOT / (c["path"].lstrip("/") + ".html")
    out.write_text(page_html(lang, head, body), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))

def build_intro(lang):
    c = C[lang]; base = c["base"]
    pre = PRE.replace("<h1>", '<h2 class="bk-h-pre">').replace("</h1>", "</h2>")
    intro = INTRO.replace("<h2>", "<h3>").replace("</h2>", "</h3>")
    intro = re.sub(r"<h1>.*?</h1>\n<p><em>The Forces Within Us</em></p>\n", "", intro, count=1)
    intro = intro.replace("<p>What This Book Is Not:</p>\n", "", 1)
    cta = f'<a class="bk-btn bk-btn-gold" href="{AMAZON}" target="_blank" rel="noopener" data-after="{E(c["cta_after"])}">{E(c["cta"])}</a>'
    body = f"""<section class="bk-ix">
  <div class="bk-head">
    <a class="back" href="{base}/book">← {E(c["ix_back"])}</a><br>
    <span class="bk-kick"><i></i>{E(c["ix_kick"])}</span>
    <h1 lang="en">Introduction: The Universe Before the Big Bang</h1>
    <p class="sub" lang="en">The Forces Within Us</p>
    <p class="note">{E(c["ix_note"])}</p>
  </div>
  <div class="bk-rule"></div>
  <article class="bk-essay" lang="en">
<div class="bk-pre">
{pre}</div>
{intro}
  </article>
  <aside class="bk-ixend bk-navy">
    <img src="/images/book/cover-3d-sm.webp" width="96" height="156" alt="" loading="lazy">
    <div class="t">
      <p class="h">{E(c["ix_end_h"])}</p>
      <p class="p">{E(c["ix_end_p"])}</p>
      <div class="bk-ctas">{cta}<a class="bk-btn bk-btn-ghost" href="{base}/book">{E(c["ix_back"])}</a></div>
    </div>
  </aside>
</section>"""
    head = head_html(lang, c["ix_title"], c["ix_desc"], c["ix_path"], c["ix_title"].split(" | ")[0], book_ld(SITE + c["path"]), [("en", "/book/introduction"), ("es", "/es/book/introduction"), ("pt", "/pt/book/introduction")])
    out = ROOT / (base.lstrip("/") + ("/" if base else "") + "book-introduction.html")
    out.write_text(page_html(lang, head, body), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))

if __name__ == "__main__":
    for lang in ("en", "es", "pt"):
        build_landing(lang)
        # build_intro(lang)  # /book/introduction retirada por ahora (Regina, 17-sep)

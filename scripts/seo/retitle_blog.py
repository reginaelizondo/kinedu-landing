#!/usr/bin/env python3
"""Títulos y descripciones del blog sin guion largo y sin quedar cortados en Google
(recomendación 1 del Estratega, semana del 6-oct-2026, aprobada por Regina el 6-oct).

1. Sufijo de marca: " — Kinedu Blog", " | Kinedu Blog" y " | Blog Kinedu" pasan a " | Kinedu"
   en <title>, og:title, twitter:title, og:image:alt y el headline del JSON-LD (mismo texto).
2. Guion largo dentro del título (" — ") pasa a ": " (o se quita en el caso de SIDS).
3. Descripciones con guion largo: texto nuevo a mano (DESCS), y og/twitter:description
   se regeneran desde la descripción cuando traían guion.
4. Los 10 posts con más impresiones y peor CTR: título y descripción nuevos (MANUAL).
Idempotente. Solo toca archivos rastreados por git en blog/, es/blog/ y pt/blog/."""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def esc(s): return s.replace("&", "&amp;").replace('"', "&quot;")
def unesc(s): return s.replace("&quot;", '"').replace("&#x27;", "'").replace("&#39;", "'").replace("&amp;", "&")

def trim(s, n=150):
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n: return s
    cut = s[:n]
    m = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if m >= 80: return cut[:m + 1]
    return cut[:cut.rfind(" ")].rstrip(",;:") + "…"

# ruta sin .html -> (título nuevo, descripción nueva)
MANUAL = {
  "pt/blog/atividades-primavera-educacao-infantil": ("4 atividades de primavera para educação infantil | Kinedu",
    "Quatro atividades de primavera prontas para a educação infantil: materiais simples, passo a passo e o que cada uma estimula."),
  "es/blog/mollera-sumida": ("Mollera sumida: causas y cuándo ir al pediatra | Kinedu",
    "Qué significa la mollera sumida en bebés, qué señales revisar en casa y cuándo conviene llamar al pediatra."),
  "es/blog/dolor-de-pechos-embarazo": ("Dolor de pechos en el embarazo: cuándo empieza | Kinedu",
    "Cuándo empieza la sensibilidad en los pechos durante el embarazo, por qué ocurre, cómo aliviarla y qué señales conviene revisar con tu médico."),
  "es/blog/indicadores-del-desarrollo-control-de-la-cabeza": ("¿A qué edad sostienen la cabeza los bebés? | Kinedu",
    "A qué edad los bebés sostienen la cabeza, la progresión mes a mes, cómo hacer tummy time y qué conviene comentar con tu pediatra."),
  "blog/baby-fake-cough": ("Baby Fake Cough: Why They Do It and When to Worry | Kinedu",
    "That little fake cough is usually your baby getting your attention, playing, or practicing sounds. Learn why they do it and what to watch for."),
  "pt/blog/bebe-sente-fome-na-barriga-da-mae": ("O bebê sente fome na barriga da mãe? | Kinedu",
    "O bebê é alimentado sem parar pela placenta, por isso não sente fome quando você sente. Veja o que acontece quando você demora para comer."),
  "pt/blog/formula-com-agua-fria": ("Pode preparar fórmula com água fria? | Kinedu",
    "Por que a temperatura da água importa no preparo da fórmula, como fazer com segurança e o que dizem as recomendações atuais."),
  "pt/blog/por-que-meu-bebe-fica-com-as-maos-fechadas-2": ("Por que o bebê fica com as mãos fechadas? | Kinedu",
    "As mãos fechadas são um reflexo do recém-nascido e vão abrindo por volta dos 5 a 6 meses. Veja como estimular as mãozinhas em cada fase."),
  "pt/blog/tamanho-do-bebe": ("Tamanho do bebê semana a semana | Kinedu",
    "O tamanho do bebê semana a semana comparado com frutas, como o ultrassom mede e em que semanas ele cresce mais."),
  "blog/baby-hungry-during-pregnancy": ("Does My Baby Get Hungry During Pregnancy? | Kinedu",
    "Your baby feeds continuously through the placenta, so they do not go hungry when you do. How nutrients reach them and how to handle cravings."),
}

# ruta sin .html -> descripción nueva (las 60 que traían guion largo)
DESCS = {
  "blog/activities-for-2-year-olds-2": "At two, attention is short and play is loud. Lean in: these activities channel the chaos into real growth.",
  "blog/breastfeeding-diet-plan": "What you eat affects your milk and your energy. Here's a practical, realistic diet plan for nursing moms.",
  "blog/category/breastfeeding": "Latching, pumping, formula and starting solids: feeding guidance from IBCLCs and pediatricians. 45 articles by pediatricians and child development experts.",
  "blog/category/child-development": "How your baby grows: what's normal, what's next, and how to support every stage. 51 articles by pediatricians and child development experts.",
  "blog/category/key-milestones": "The big moments of your baby's first years: when they happen and what to expect. 34 articles by pediatricians and child development experts.",
  "blog/category/linguistic": "From first babbles to first sentences: speech milestones and how to encourage talking. 62 articles by pediatricians and child development experts.",
  "blog/category/physical": "Rolling, crawling, walking and motor skills: milestones and activities to support movement. 81 articles by pediatricians and child development experts.",
  "blog/category/safety": "Babyproofing, safe sleep, car seats and first aid: keeping your little one safe. 26 articles by pediatricians and child development experts.",
  "blog/category/sleep": "Sleep regressions, naps, bedtime routines and night wakings: expert answers for tired parents. 42 articles by pediatricians and child development experts.",
  "blog/category/socialandemotional": "Bonding, emotions, tantrums and social skills: raising emotionally healthy kids. 113 articles by pediatricians and child development experts.",
  "blog/does-my-little-one-have-nightmares": "Childhood nightmares: how they affect sleep and emotions, and when they typically begin.",
  "blog/happy-healthy-pregnancy": "Hello, future mom! During pregnancy you can expect lots of changes and emotions. It's like a rollercoaster, but also a stage filled with magic.",
  "blog/help-my-baby-will-not-sleep": "Separation anxiety and bedtime: babies around a year old might resist bedtime due to separation anxiety, a normal sign of healthy attachment.",
  "blog/how-does-your-babys-vision-develop": "Your baby can barely see at birth, but their visual system develops at a breathtaking pace in the first year.",
  "blog/how-serious-is-postpartum-preeclampsia": "Pregnancy and motherhood come with so much joy, and sometimes a lot of worries. What postpartum preeclampsia is, its warning signs and when to call your doctor.",
  "blog/how-to-burp-a-baby": "Burping seems simple, but technique matters. Here are the three most effective positions, explained clearly.",
  "blog/how-to-help-your-child-to-stop-wetting-the-bed": "If nighttime puddles and endless laundry feel like the norm in your house, don't worry: you're not alone!",
  "blog/how-to-recover-after-a-c-section": "C-section recovery is a major physical process, and one that's often underestimated. Here's a week-by-week guide.",
  "blog/postpartum-physical-therapy-the-unsung-hero-of-post-baby-recovery": "Having a baby is a monumental moment, but let's be real: it's also a full-body workout that leaves you sore in places you didn't even know existed.",
  "blog/signs-of-colic-in-babies": "Colic is one of the most stressful experiences in new parenthood. Here's how to identify it, and what actually helps.",
  "blog/stage/baby": "Milestones, solids, sleep and play for babies 4 to 12 months old: expert guidance for the first year. 370 articles by pediatricians and child development experts.",
  "blog/stage/newborn": "Sleep, feeding, reflexes and caring for your newborn: expert answers for the first three months. 80 articles by pediatricians and child development experts.",
  "blog/stage/prenatal": "Pregnancy week by week, prenatal health and getting ready for baby: expert answers for every stage of pregnancy. 143 articles by pediatricians and child development experts.",
  "blog/stage/toddler": "Tantrums, language, potty training and play for toddlers 1 to 3 years old: expert answers for the toddler years. 103 articles by pediatricians and child development experts.",
  "blog/what-do-i-do-if-my-baby-ate-sand": "Most babies who taste dirt or sand are completely fine. It can even support their immune system. Here's what to do and which precautions to take outside.",
  "blog/what-should-a-6-month-old-feeding-schedule-look-like": "Six months is a big milestone: solid foods enter the picture. Here's how to structure the day.",
  "blog/when-do-babies-sleep-through-the-night": "A full night of sleep is coming, but maybe not when you think. Here's the honest timeline every new parent needs.",
  "blog/when-to-see-a-lactation-consultant": "Breastfeeding is natural, but it's not always easy. Here's when to call in a pro, and what to expect.",
  "blog/white-noise-for-babies": "White noise can be a game-changer for sleep, but is it safe? Here's the science, and how to use it right.",
  "blog/why-does-the-12-month-sleep-regression-occur": "The first birthday sleep slump is one of the most common regressions, and the least talked about. Here's the full picture.",
  "blog/why-does-the-4-month-sleep-regression-happen": "The 4-month regression is real, and it's actually a sign your baby's brain is growing fast. Here's what to expect.",
  "blog/why-does-the-6-month-sleep-regression-happen": "Just when sleep was getting better, it falls apart again. Here's why, and how to get through it.",
  "blog/why-does-the-8-10-month-sleep-regression-happen": "Crawling, pulling up, separation anxiety: your baby's brain is on overdrive. No wonder sleep suffers.",
  "blog/your-babys-first-words": "From cooing to \"mama\": the science of how language develops and how you can boost it every day.",
  "es/blog/category/desarrollo-infantil": "Cómo crece tu bebé: qué es normal, qué sigue y cómo apoyar cada etapa. 70 artículos de expertas.",
  "es/blog/category/fisica": "Rodar, gatear, caminar y habilidades motoras: hitos y actividades de movimiento. 92 artículos de expertas.",
  "es/blog/category/leche-materna": "Agarre, extracción, fórmula y alimentación: guía de consultoras certificadas. 39 artículos de expertas.",
  "es/blog/category/linguistica": "De los primeros balbuceos a las primeras frases: hitos del lenguaje. 53 artículos de expertas.",
  "es/blog/category/socio-afectiva": "Vínculo, emociones, berrinches y habilidades sociales: cría niños emocionalmente sanos. 120 artículos de expertas.",
  "es/blog/collage-para-ninos": "Cuatro ideas de collage fáciles de hacer en casa, como el de alimentos nutritivos con recortes de revistas, para estimular la creatividad y el aprendizaje de tu hijo mientras se divierte.",
  "es/blog/ejercicio-y-cuidado-corporal-durante-el-posparto-cuidando-de-ti": "Hola, mamá, ¡felicidades por tu bebé! Has logrado algo increíble y ahora es momento de enfocarte en ti. El posparto es un torbellino emocional, físico y mental. Aquí te decimos cómo cuidarte.",
  "es/blog/stage/prenatal": "Nutrición, ejercicio, bienestar y preparación para el parto: guía experta para tu embarazo.",
  "es/blog/stage/recien-nacido": "Sueño, lactancia, apego y los primeros hitos: todo sobre las primeras 12 semanas.",
  "es/blog/trastorno-del-sueno-en-bebes": "Según la Academia Americana de Pediatría, los pequeños deben dormir un total de 12 a 16 horas al día, incluyendo siestas, hasta cumplir los 12 meses.",
  "pt/blog/as-diferentes-maneiras-e-estilos-na-hora-de-engatinhar-2-2": "Seu bebê está pronto para engatinhar? Nem todos aprendem a se movimentar do modo tradicional: muitos desenvolvem estilos únicos de locomoção, e tudo bem!",
  "pt/blog/calculadora-gestacional": "Descubra com quantas semanas de gravidez você está, converta semanas em meses e veja a data provável do parto, com calculadora interativa e tabela por trimestre.",
  "pt/blog/category/amamentacao": "Pega, extração, fórmula e alimentação: orientação de consultoras certificadas. 58 artigos de especialistas.",
  "pt/blog/category/fisico": "Rolar, engatinhar, andar e habilidades motoras: marcos e atividades de movimento. 135 artigos de especialistas.",
  "pt/blog/category/linguistico": "Dos primeiros balbucios às primeiras frases: marcos da linguagem. 83 artigos de especialistas.",
  "pt/blog/category/socioafetivo": "Vínculo, emoções, birras e habilidades sociais: crie crianças emocionalmente saudáveis. 145 artigos de especialistas.",
  "pt/blog/como-ajudar-seu-filho-a-parar-de-fazer-xixi-na-cama": "Se as poças noturnas e a pilha de roupas para lavar parecem a norma na sua casa, não se preocupe: você não está sozinha! Fazer xixi na cama é uma parte normal do crescimento de muitas crianças.",
  "pt/blog/convivencia-com-outras-criancas": "O ser humano é um ser sociável. Mais do que nos relacionar com outras pessoas, precisamos estar em sociedade para ter nossas necessidades de interação atendidas, inclusive as de afeto.",
  "pt/blog/doenca-mao-pe-boca-o-que-todo-pai-e-mae-deve-saber": "Se você tem filhos na creche ou na pré-escola, provavelmente já ouviu falar da Doença Mão-Pé-Boca. Só de ouvir falar dela pode bater uma certa preocupação. Mas calma! Veja o que todo pai e mãe deve saber.",
  "pt/blog/exercicio-e-cuidados-com-o-corpo-no-pos-parto-cuidando-de-voce": "Olá, mamãe, parabéns pelo seu bebê! Você realizou algo incrível, e agora é hora de focar em você. O pós-parto é um turbilhão emocional, físico e mental. Veja como cuidar do seu corpo.",
  "pt/blog/meu-bebe-tem-pesadelos": "Pesadelos infantis: entenda como afetam o sono e as emoções, e quando geralmente começam.",
  "pt/blog/power-pump": "Power pump é uma técnica de ordenha em ciclos curtos (regra 10-10-10: 10 minutos bombeando, 10 de pausa, mais 10 bombeando, por cerca de uma hora) para estimular a produção de leite. Veja como fazer e com que frequência.",
  "pt/blog/salto-de-desenvolvimento": "Durante um salto de desenvolvimento o bebê aprende habilidades novas de forma intensa e fica mais agitado. Veja em que semanas acontecem, até por volta das 75 semanas, e como identificar cada um.",
  "pt/blog/stage/pre-natal": "Nutrição, exercícios, bem-estar e preparação para o parto: orientação especializada para sua gestação.",
  "pt/blog/stage/recem-nascido": "Sono, amamentação, vínculo e os primeiros marcos: tudo sobre as primeiras 12 semanas.",
}

SUFFIX = re.compile(r" (?:—|\|) (?:Kinedu Blog|Blog Kinedu)$")

def new_title(old):
    t = SUFFIX.sub(" | Kinedu", old)
    t = t.replace(" — and ", " and ")       # "What Causes SIDS — and How Can I Prevent It?"
    t = t.replace(" — ", ": ")
    return t

def get_meta(html, attr, key):
    m = re.search(r'<meta\s+%s="%s"\s+content="([^"]*)"' % (attr, re.escape(key)), html)
    return m.group(1) if m else None

def set_meta(html, attr, key, value):
    pat = re.compile(r'(<meta\s+%s="%s"\s+content=")[^"]*(")' % (attr, re.escape(key)))
    return pat.sub(lambda m: m.group(1) + esc(value) + m.group(2), html, count=1)

def replace_everywhere(html, old, new):
    """Reemplaza el texto del título en title, metas, JSON-LD y alt: cualquier aparición
    delimitada por comillas o por < >, tanto escapado como sin escapar."""
    for o, n in ((old, new), (unesc(old), unesc(new)), (esc(unesc(old)), esc(unesc(new)))):
        if o == n: continue
        html = re.sub(r'(?<=["<>])' + re.escape(o) + r'(?=["<])', lambda m: n, html)
    return html

def process(rel):
    fp = os.path.join(ROOT, rel)
    html = open(fp, encoding="utf-8").read(); orig = html
    key = rel[:-5]
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m: return False, "sin title"
    old_t = m.group(1).strip()
    notes = []
    if key in MANUAL:
        nt, nd = MANUAL[key]
        html = replace_everywhere(html, old_t, esc(nt))
        html = set_meta(html, "name", "description", nd)
        html = set_meta(html, "property", "og:description", trim(nd))
        html = set_meta(html, "name", "twitter:description", trim(nd))
        notes.append("manual")
    else:
        nt = new_title(old_t)
        if nt != old_t:
            html = replace_everywhere(html, old_t, nt); notes.append("título")
        if key in DESCS:
            html = set_meta(html, "name", "description", DESCS[key]); notes.append("descripción")
        d = get_meta(html, "name", "description")
        for attr, k in (("property", "og:description"), ("name", "twitter:description")):
            v = get_meta(html, attr, k)
            if v and "—" in v and d:
                html = set_meta(html, attr, k, trim(unesc(d))); notes.append(k)
    # Páginas de categoría y etapa: og:title / twitter:title / og:image:alt venían con otro
    # texto (y a veces en otro idioma) y con guion largo; se igualan al <title> nuevo.
    cur_t = unesc(re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip())
    for attr, k in (("property", "og:title"), ("name", "twitter:title"), ("property", "og:image:alt")):
        v = get_meta(html, attr, k)
        if v and "—" in v:
            html = set_meta(html, attr, k, cur_t); notes.append(k)
    if html != orig:
        open(fp, "w", encoding="utf-8").write(html); return True, ", ".join(notes)
    return False, ""

if __name__ == "__main__":
    files = subprocess.run(["git", "ls-files", "blog", "es/blog", "pt/blog"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    files = [f for f in files if f.endswith(".html")]
    changed = 0; manual = 0
    for f in files:
        ok, note = process(f)
        if ok:
            changed += 1
            if "manual" in note: manual += 1; print("  manual:", f)
    print("archivos cambiados: %d de %d (manuales: %d)" % (changed, len(files), manual))
    # Lo que queda con guion largo en title / metas
    left = []
    for f in files:
        h = open(os.path.join(ROOT, f), encoding="utf-8").read()
        for pat in (r"<title>[^<]*—[^<]*</title>", r'<meta[^>]+(?:description|og:title|twitter:title|og:image:alt)"\s+content="[^"]*—[^"]*"'):
            if re.search(pat, h): left.append(f); break
    print("quedan con guion largo en title/metas:", len(left))
    for f in left[:20]: print("  ", f)

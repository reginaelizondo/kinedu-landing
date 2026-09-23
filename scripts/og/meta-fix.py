#!/usr/bin/env python3
"""Normaliza los metatags de preview (Open Graph + Twitter) de todo el sitio.

- Páginas principales: og:description/twitter:description CORTAS (lo que
  WhatsApp/iMessage muestran), og:image por idioma, og:image:width/height/alt,
  twitter:card/title/description/image completos.
- Quiz y páginas de ads: bloque completo.
- Blog (EN/ES/PT): recorta og/twitter:description a 150 caracteres y agrega
  og:image:width/height leyendo la imagen local de blog-media.
Idempotente: se puede correr las veces que haga falta."""
import glob, os, re, struct, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://www.kinedu.com"

# path -> (og:image, descripción corta)  (None = conservar la actual)
PAGES = {
  "index.html":      ("og-image.png",    "Daily activity plans, milestone tracking and live expert classes for your baby. Trusted by 11M+ families."),
  "es/index.html":   ("og-image-es.png", "Plan diario de actividades, seguimiento de hitos y clases en vivo con expertos. +11M de familias confían en Kinedu."),
  "pt/index.html":   ("og-image-pt.png", "Plano diário de atividades, marcos do desenvolvimento e aulas ao vivo com especialistas. 11M+ famílias confiam no Kinedu."),
  "book.html":       ("og-book.png",     "The science of how your child’s universe takes shape, by Kinedu founder Luis Garza Sada. Available now on Amazon."),
  "es/book.html":    ("og-book-es.png",  "La ciencia detrás del universo de tu hijo, por Luis Garza Sada, fundador de Kinedu. Ya disponible en Amazon."),
  "pt/book.html":    ("og-book-pt.png",  "A ciência por trás do universo do seu filho, por Luis Garza Sada, fundador do Kinedu. Já disponível na Amazon."),
  "gift.html":       ("og-gift.png",     "Give a new parent a full year of Kinedu. Write a note, pick the day, and we deliver it by email."),
  "es/gift.html":    ("og-gift-es.png",  "Regala un año completo de Kinedu. Escribe una nota, elige el día y lo entregamos por correo."),
  "pt/gift.html":    ("og-gift-pt.png",  "Presenteie um ano inteiro de Kinedu. Escreva uma mensagem, escolha o dia e entregamos por e-mail."),
  "live-classes.html":    ("og-live-classes.png",    "Pediatricians, sleep coaches and feeding experts, live every day. Bring your question, leave with an answer."),
  "es/live-classes.html": ("og-live-classes-es.png", "Pediatras, coaches de sueño y expertas en alimentación, en vivo cada día. Trae tu duda y sal con una respuesta."),
  "pt/live-classes.html": ("og-live-classes-pt.png", "Pediatras, coaches de sono e especialistas em alimentação, ao vivo todos os dias. Traga sua dúvida e saia com uma resposta."),
  "live-classes-ads-en.html": ("og-live-classes.png",    "Pediatricians, sleep coaches and feeding experts, live every day. Bring your question, leave with an answer."),
  "live-classes-ads-es.html": ("og-live-classes-es.png", "Pediatras, coaches de sueño y expertas en alimentación, en vivo cada día. Trae tu duda y sal con una respuesta."),
  "live-classes-ads-pt.html": ("og-live-classes-pt.png", "Pediatras, coaches de sono e especialistas em alimentação, ao vivo todos os dias. Traga sua dúvida e saia com uma resposta."),
  "science.html":    ("og-science.png",    "How we built a clearer picture of your baby’s development, with data from 3.5 million children. Part 1 of 3."),
  "es/science.html": ("og-science-es.png", "Cómo construimos una imagen más clara del desarrollo de tu bebé, con datos de 3.5 millones de niños. Parte 1 de 3."),
  "pt/science.html": ("og-science-pt.png", "Como construímos uma imagem mais clara do desenvolvimento do seu bebê, com dados de 3,5 milhões de crianças. Parte 1 de 3."),
  "science-what-we-know.html":    ("og-science-what-we-know.png",    "Five things we’ve learned about how babies develop. The science behind Kinedu, part 2 of 3."),
  "es/science-what-we-know.html": ("og-science-what-we-know-es.png", "Cinco cosas que hemos aprendido sobre cómo se desarrollan los bebés. La ciencia detrás de Kinedu, parte 2 de 3."),
  "pt/science-what-we-know.html": ("og-science-what-we-know-pt.png", "Cinco coisas que aprendemos sobre como os bebês se desenvolvem. A ciência por trás do Kinedu, parte 2 de 3."),
  "science-what-you-can-do.html":    ("og-science-what-you-can-do.png",    "Four ways to support your child’s development, backed by what we’ve learned. Part 3 of 3."),
  "es/science-what-you-can-do.html": ("og-science-what-you-can-do-es.png", "Cuatro formas de apoyar el desarrollo de tu hijo, respaldadas por lo que hemos aprendido. Parte 3 de 3."),
  "pt/science-what-you-can-do.html": ("og-science-what-you-can-do-pt.png", "Quatro maneiras de apoiar o desenvolvimento do seu filho, com base no que aprendemos. Parte 3 de 3."),
  "masterclasses.html":    ("og-masterclasses.png",    "Video courses by certified experts: newborn first aid, sleep, feeding and development. Watch on your schedule."),
  "es/masterclasses.html": ("og-masterclasses-es.png", "Cursos en video con expertos certificados: primeros auxilios, sueño, alimentación y desarrollo. A tu ritmo."),
  "pt/masterclasses.html": ("og-masterclasses-pt.png", "Cursos em vídeo com especialistas certificados: primeiros socorros, sono, alimentação e desenvolvimento. No seu ritmo."),
  "experts.html":    ("og-experts.png",  "Pediatricians, sleep consultants, lactation experts and child psychologists. The team behind Kinedu."),
  "founder.html":    ("og-image.png",    None),
  "articles.html":    ("og-blog.png",    "Real guidance for real parents: sleep, feeding, milestones and play, by Kinedu’s experts."),
  "es/articles.html": ("og-blog-es.png", "Guía real para padres reales: sueño, alimentación, hitos y juego, por los expertos de Kinedu."),
  "pt/articles.html": ("og-blog-pt.png", "Orientação real para pais reais: sono, alimentação, marcos e brincadeiras, pelos especialistas do Kinedu."),
  "browse.html":    ("og-blog.png",    None), "es/browse.html": ("og-blog-es.png", None), "pt/browse.html": ("og-blog-pt.png", None),
  "privacy.html":   ("og-image.png",   None), "es/privacy.html": ("og-image-es.png", None), "pt/privacy.html": ("og-image-pt.png", None),
  "terms.html":     ("og-image.png",   None), "es/terms.html":   ("og-image-es.png", None), "pt/terms.html":   ("og-image-pt.png", None),
  "quiz-en.html":   ("og-live-classes.png",    "Answer 3 questions and find out which live expert classes are right for your baby. Free."),
  "quiz-es.html":   ("og-live-classes-es.png", "Responde 3 preguntas y descubre qué clases en vivo con expertos son para tu bebé. Gratis."),
  "quiz-pt.html":   ("og-live-classes-pt.png", "Responda 3 perguntas e descubra quais aulas ao vivo com especialistas são para o seu bebê. Grátis."),
}
# La meta description (SEO) del libro también decía "pre-order"; hoy ya salió.
BOOK_DESC = {
  "book.html":    ("Read an excerpt and pre-order the book.", "Read an excerpt and get it on Amazon."),
  "es/book.html": ("Lee un extracto y reserva el libro.", "Lee un extracto y cómpralo en Amazon."),
  "pt/book.html": ("Leia um trecho e reserve o livro.", "Leia um trecho e compre na Amazon."),
}

def esc(s): return s.replace("&", "&amp;").replace('"', "&quot;")
def unesc(s): return s.replace("&quot;", '"').replace("&#39;", "'").replace("&amp;", "&")

def get_meta(html, attr, key):
    m = re.search(r'<meta\s+%s="%s"\s+content="([^"]*)"' % (attr, re.escape(key)), html)
    return unesc(m.group(1)) if m else None

def set_meta(html, attr, key, value, after_key=None, after_attr="property", indent=""):
    """Reemplaza el content de la meta o la inserta después de after_key."""
    tag = '<meta %s="%s" content="%s">' % (attr, key, esc(value))
    pat = re.compile(r'<meta\s+%s="%s"\s+content="[^"]*"\s*/?>' % (attr, re.escape(key)))
    if pat.search(html):
        return pat.sub(lambda m: tag, html, count=1)
    if after_key:
        apat = re.compile(r'([ \t]*)<meta\s+%s="%s"\s+content="[^"]*"\s*/?>' % (after_attr, re.escape(after_key)))
        m = apat.search(html)
        if m:
            return html[:m.end()] + "\n" + m.group(1) + tag + html[m.end():]
    m = re.search(r'</title>', html)
    return html[:m.end()] + "\n" + indent + tag + html[m.end():]

def page_url(path):
    p = "/" + path[:-5]
    if p.endswith("/index"): p = p[:-6] or "/"
    return SITE + p

def fix_page(path, img, short):
    fp = os.path.join(ROOT, path)
    html = open(fp, encoding="utf-8").read(); orig = html
    title = get_meta(html, "property", "og:title") or re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", html, re.S).group(1)).strip()
    desc = short or get_meta(html, "property", "og:description") or get_meta(html, "name", "description") or ""
    if path in BOOK_DESC:
        a, b = BOOK_DESC[path]; html = html.replace(a, b)
    if not get_meta(html, "name", "description"):
        html = set_meta(html, "name", "description", desc)
    # Bloque OG en orden; cada set_meta reemplaza si existe o inserta tras la anterior.
    html = set_meta(html, "property", "og:title", title, after_key="description", after_attr="name")
    html = set_meta(html, "property", "og:description", desc, after_key="og:title")
    html = set_meta(html, "property", "og:image", SITE + "/" + img, after_key="og:description")
    html = set_meta(html, "property", "og:image:width", "1200", after_key="og:image")
    html = set_meta(html, "property", "og:image:height", "630", after_key="og:image:width")
    html = set_meta(html, "property", "og:image:alt", title, after_key="og:image:height")
    if not get_meta(html, "property", "og:url"):
        html = set_meta(html, "property", "og:url", page_url(path), after_key="og:image:alt")
    if not get_meta(html, "property", "og:type"):
        html = set_meta(html, "property", "og:type", "website", after_key="og:url")
    if not get_meta(html, "property", "og:site_name"):
        html = set_meta(html, "property", "og:site_name", "Kinedu", after_key="og:type")
    html = set_meta(html, "name", "twitter:card", "summary_large_image", after_key="og:site_name")
    html = set_meta(html, "name", "twitter:title", title, after_key="twitter:card", after_attr="name")
    html = set_meta(html, "name", "twitter:description", desc, after_key="twitter:title", after_attr="name")
    html = set_meta(html, "name", "twitter:image", SITE + "/" + img, after_key="twitter:description", after_attr="name")
    if html != orig:
        open(fp, "w", encoding="utf-8").write(html); return True
    return False

# ---------- blog ----------
def img_dims(local):
    try:
        with open(local, "rb") as f: d = f.read(64 * 1024)
    except OSError: return None
    if d[:8] == b"\x89PNG\r\n\x1a\n": return struct.unpack(">II", d[16:24])
    if d[:4] == b"RIFF" and d[8:12] == b"WEBP":
        if d[12:16] == b"VP8X": return (int.from_bytes(d[24:27], "little") + 1, int.from_bytes(d[27:30], "little") + 1)
        if d[12:16] == b"VP8 ": return (struct.unpack("<H", d[26:28])[0] & 0x3fff, struct.unpack("<H", d[28:30])[0] & 0x3fff)
        if d[12:16] == b"VP8L":
            b = d[21:25]; return (1 + (((b[1] & 0x3F) << 8) | b[0]), 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6)))
    if d[:2] == b"\xff\xd8":
        i = 2
        while i < len(d) - 9:
            if d[i] != 0xFF: i += 1; continue
            marker = d[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", d[i + 5:i + 9]); return (w, h)
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7: i += 2; continue
            i += 2 + struct.unpack(">H", d[i + 2:i + 4])[0]
    return None

def trim(s, n=150):
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n: return s
    cut = s[:n]
    m = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if m >= 80: return cut[:m + 1]
    return cut[:cut.rfind(" ")].rstrip(",;:") + "…"

DIMS = {}
def fix_blog(fp):
    html = open(fp, encoding="utf-8").read(); orig = html
    for attr, key in (("property", "og:description"), ("name", "twitter:description")):
        v = get_meta(html, attr, key)
        if v and len(v) > 150: html = set_meta(html, attr, key, trim(v))
    img = get_meta(html, "property", "og:image")
    if img and not get_meta(html, "property", "og:image:width"):
        m = re.search(r"-(\d{2,4})x(\d{2,4})\.(?:jpe?g|png|webp)$", img, re.I)
        dims = (int(m.group(1)), int(m.group(2))) if m else None
        if not dims and img.startswith(SITE + "/"):
            local = os.path.join(ROOT, img[len(SITE) + 1:])
            dims = DIMS.get(local) or DIMS.setdefault(local, img_dims(local))
        if dims:
            html = set_meta(html, "property", "og:image:width", str(dims[0]), after_key="og:image")
            html = set_meta(html, "property", "og:image:height", str(dims[1]), after_key="og:image:width")
    if html != orig:
        open(fp, "w", encoding="utf-8").write(html); return True
    return False

if __name__ == "__main__":
    n = sum(fix_page(p, i, d) for p, (i, d) in PAGES.items())
    print("páginas principales cambiadas:", n)
    if "--no-blog" not in sys.argv:
        files = [f for d in ("blog", "es/blog", "pt/blog") for f in glob.glob(os.path.join(ROOT, d, "*.html"))]
        print("blog cambiados:", sum(fix_blog(f) for f in files), "de", len(files))

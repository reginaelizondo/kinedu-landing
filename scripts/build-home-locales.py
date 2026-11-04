# Genera es/index.html y pt/index.html a partir de index.html.
# 1) <head> localizado (title, description, OG, canonical, lang) y rutas absolutas (como antes).
# 2) NUEVO (nov-2026): el BODY sale ya traducido en el HTML (sin depender de translations.js):
#    se aplica exactamente lo que hace applyTranslations() de script.js en el navegador
#    (data-i18n -> textContent, data-i18n-html -> innerHTML, data-i18n-href -> href,
#    problem.words -> spans .word) para que los bots que no ejecutan JS (OpenAI, Anthropic,
#    Perplexity) lean la landing en su idioma. Los atributos data-i18n se conservan: el JS
#    en runtime vuelve a poner el mismo texto (no-op) y el cambio de idioma sigue funcionando.
# 3) NUEVO: FAQPage JSON-LD estatico (id kinedu-faq-static) con las FAQ del idioma; el loader
#    client-side (kinedu-faq-ld) no lo duplica si ya existe.
# Uso: python3 scripts/build-home-locales.py   (idempotente; correr tras editar index.html o translations.js)
import re, json, os, html, subprocess, sys

L = "/Users/reginaelizondo/Desktop/CLAUDE/Landing Page"
src = open(L + "/index.html", encoding="utf-8").read()

# --- diccionarios: se evaluan con node para no parsear JS a mano ---
T = json.loads(subprocess.check_output(
    ["node", "-e", "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.TRANSLATIONS))", L + "/translations.js"],
    text=True))
assert all(k in T for k in ("en", "es", "pt")), T.keys()

VOID = {"img", "input", "br", "hr", "meta", "link", "source", "track", "wbr", "area", "base", "col", "embed", "param"}
OPEN_RE = re.compile(r'<([a-zA-Z][a-zA-Z0-9-]*)(\s[^<>]*?)?>')

def find_close(s, tag, start):
    """indice del '</tag>' que cierra el elemento abierto justo antes de start (cuenta anidados)."""
    depth = 1
    pat = re.compile(r'<(/?)' + re.escape(tag) + r'(?=[\s>/])[^<>]*>', re.I)
    pos = start
    while True:
        m = pat.search(s, pos)
        if not m:
            raise ValueError("sin cierre para <%s>" % tag)
        if m.group(1) == '/':
            depth -= 1
            if depth == 0:
                return m.start(), m.end()
        else:
            if not m.group(0).endswith('/>'):
                depth += 1
        pos = m.end()

def problem_words_html(words, indent):
    return "\n".join(indent + '<span class="word%s">%s</span>' % (" accent" if w.get("a") else "", html.escape(w["t"], quote=False)) for w in words) + "\n" + indent[:-4]

def bake(s, t, lang):
    out, pos, n_text, n_html, n_href = [], 0, 0, 0, 0
    while True:
        m = OPEN_RE.search(s, pos)
        if not m:
            out.append(s[pos:]); break
        tag, attrs = m.group(1).lower(), m.group(2) or ""
        km = re.search(r'\sdata-i18n="([^"]+)"', attrs)
        hm = re.search(r'\sdata-i18n-href="([^"]+)"', attrs)
        if not km and not hm:
            out.append(s[pos:m.end()]); pos = m.end(); continue
        open_tag = m.group(0)
        if hm and hm.group(1) in t:
            v = t[hm.group(1)]
            open_tag2 = re.sub(r'\shref="[^"]*"', ' href="%s"' % html.escape(v, quote=True), open_tag, count=1)
            if open_tag2 != open_tag: n_href += 1
            open_tag = open_tag2
        out.append(s[pos:m.start()]); out.append(open_tag); pos = m.end()
        if not km or tag in VOID or open_tag.endswith('/>'):
            continue
        key = km.group(1)
        if key not in t:
            continue
        c0, c1 = find_close(s, tag, pos)
        inner = s[pos:c0]
        if key == "problem.words":
            indent = re.match(r'\s*', inner).group(0)
            indent = indent[indent.rfind("\n") + 1:] if "\n" in indent else "                "
            new = "\n" + problem_words_html(t[key], indent)
            n_html += 1
        elif re.search(r'\sdata-i18n-html(?=[\s>=]|$)', attrs):
            new = t[key]; n_html += 1
        else:
            new = html.escape(t[key], quote=False); n_text += 1
        out.append(new); out.append(s[c0:c1]); pos = c1
    return "".join(out), (n_text, n_html, n_href)

def faq_ld(t):
    qs = sorted({int(k[5:]) for k in t if re.fullmatch(r'faq\.q\d+', k)})
    main = []
    for i in qs:
        q, a = t.get("faq.q%d" % i), t.get("faq.a%d" % i)
        if not q or not a: continue
        strip = lambda x: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(x))).strip()
        main.append({"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}})
    if len(main) < 3: return ""
    return '<script type="application/ld+json" id="kinedu-faq-static">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main}, ensure_ascii=False)

def with_static_faq(s, t):
    s = re.sub(r'<script type="application/ld\+json" id="kinedu-faq-static">.*?</script>\n?', '', s, flags=re.S)
    block = faq_ld(t)
    if not block: return s
    anchor = '<script id="kinedu-faq-ld">'
    assert anchor in s, "falta el loader kinedu-faq-ld"
    return s.replace(anchor, block + "\n" + anchor, 1)

def localize_head(s, lang):
    t = T[lang]
    # (?<![\w-]) evita tocar data-i18n-href="clave" (el generador viejo lo convertia en "/clave" y rompia los links /es/blog, /es/gift...)
    s = re.sub(r'(?<![\w-])(src|href|srcset|poster)="(?!https?:|/|#|mailto:|tel:|data:|javascript:)([^"]+)"', lambda m: '%s="/%s"' % (m.group(1), m.group(2)), s)
    s = re.sub(r"url\('(?!https?:|/|data:)([^']+)'\)", r"url('/\1')", s)
    s = s.replace('<html lang="en"', '<html lang="%s"' % lang, 1)
    title = t.get('meta.title'); d = t.get('meta.description') or t.get('hero.sub') or t.get('hero.subtitle')
    if d: d = re.sub(r'<[^>]+>', '', d).replace('\\n', ' ').strip()
    if title:
        s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, s, count=1)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + title, s)
        s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r'\g<1>' + title, s)
        s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + title, s)
    if d:
        s = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + d, s)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + d, s)
        s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', r'\g<1>' + d, s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>https://www.kinedu.com/%s' % lang, s)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\g<1>https://www.kinedu.com/%s' % lang, s)
    s = s.replace('<meta property="og:locale" content="en_US">', '<meta property="og:locale" content="%s">' % ('es_MX' if lang == 'es' else 'pt_BR'))
    s = s.replace('og-image.png', 'og-image-%s.png' % lang) if os.path.exists(L + "/og-image-%s.png" % lang) else s
    return s

if __name__ == "__main__":
    # EN: solo el FAQPage estatico (el body ya es ingles)
    en = with_static_faq(src, T["en"])
    if en != src:
        open(L + "/index.html", "w", encoding="utf-8").write(en); print("index.html: FAQPage estatico actualizado")
    src = en
    for lang in ("es", "pt"):
        s = localize_head(src, lang)
        s, stats = bake(s, T[lang], lang)
        s = with_static_faq(s, T[lang])
        s = '<!-- GENERADO desde index.html por scripts/build-home-locales.py (no editar a mano): head localizado, rutas absolutas y BODY ya traducido (los bots sin JS lo leen en %s) -->\n' % lang + s
        os.makedirs(L + "/" + lang, exist_ok=True)
        open(L + "/%s/index.html" % lang, "w", encoding="utf-8").write(s)
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        print(lang, "->", lang + "/index.html | textos:%d html:%d hrefs:%d" % stats, "| h1:", re.sub(r'<[^>]+>|\s+', ' ', h1.group(1)).strip()[:60] if h1 else "?")

# -*- coding: utf-8 -*-
import re, json, os
NUM_ONLY = re.compile(r'^[\d\s.,%:·≈–→←↓±—✓✕]+$')

def localize(html, path, lang, META, H1, T):
    LOCALE={'es':'es_MX','pt':'pt_BR'}[lang]
    missing = []
    title, desc, og = META[path]
    # ---- head ----
    html = re.sub(r'<html([^>]*)lang="en"', r'<html\1lang="%s"' % lang, html, count=1)
    html = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, html, count=1)
    html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc, html, count=1)
    for k in ("og:title", "twitter:title"):
        html = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % k, r'\g<1>' + og, html)
    for k in ("og:description", "twitter:description"):
        html = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % k, r'\g<1>' + desc, html)
    html = html.replace('<link rel="canonical" href="https://www.kinedu.com%s">' % path, '<link rel="canonical" href="https://www.kinedu.com/%s%s">' % (lang, path))
    html = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>https://www.kinedu.com/' + lang + path, html)
    html = re.sub(r'(<meta property="og:locale" content=")[^"]*', r'\g<1>' + LOCALE, html)
    _og='og-'+path.strip('/')+'-'+lang+'.png'
    if os.path.exists(os.path.join(os.path.dirname(__file__),'..','..',_og)): html=html.replace('https://www.kinedu.com/og-'+path.strip('/')+'.png','https://www.kinedu.com/'+_og)
    # JSON-LD
    def ld(m):
        d = json.loads(m.group(1))
        for it in d["itemListElement"]:
            it["name"] = T.get(it["name"], it["name"]); it["item"] = it["item"].replace("https://www.kinedu.com/", "https://www.kinedu.com/%s/" % lang)
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, html, count=1, flags=re.S)
    # ---- body ----
    i = html.index("<body")
    head, body = html[:i], html[i:]
    for en, es in H1.items(): body = body.replace(en, es)
    # proteger style/script
    blocks = []
    def keep(m): blocks.append(m.group(0)); return "\x00%d\x00" % (len(blocks) - 1)
    body = re.sub(r'<style.*?</style>', keep, body, flags=re.S)
    def sc(m):
        s = m.group(0)
        def q(mm):
            k = mm.group(1)
            return '"' + T[k] + '"' if k in T else mm.group(0)
        s = re.sub(r'"((?:[^"\\]|\\.)*)"', q, s)
        blocks.append(s); return "\x00%d\x00" % (len(blocks) - 1)
    body = re.sub(r'<script.*?</script>', sc, body, flags=re.S)
    def tx(m):
        raw = m.group(1); t = raw.strip()
        if not t or NUM_ONLY.match(t): return m.group(0)
        if t in T: return ">" + raw.replace(t, T[t]) + "<"
        if re.search(r'[A-Za-z]{3}', t) and "data-i18n" not in raw: missing.append(t)
        return m.group(0)
    body = re.sub(r'>([^<>]+)<', tx, body)
    body = re.sub(r'(aria-label|alt|title)="([^"]+)"', lambda m: '%s="%s"' % (m.group(1), T.get(m.group(2), m.group(2))), body)
    body = re.sub(r'\x00(\d+)\x00', lambda m: blocks[int(m.group(1))], body)
    # links internos de la serie y PDFs
    body = body.replace('href="/science', 'href="/%s/science' % lang)
    body = body.replace('href="/book"', 'href="/%s/book"' % lang)
    body = body.replace('/research/kinedu-replication-EXTERNAL.pdf', '/research/kinedu-replication-EXTERNAL-%s.pdf' % lang.upper()).replace('/research/kinedu-parents-guide.pdf', '/research/kinedu-parents-guide-%s.pdf' % lang.upper())
    # nav/footer: textos ES de translations.js (como en las demás páginas /es/)
    tj = open(os.path.join(os.path.dirname(__file__), "..", "..", "translations.js"), encoding="utf-8").read()
    esblk = tj[tj.index("es: {"):tj.index("pt: {")] if lang=="es" else tj[tj.index("pt: {"):]
    keys = dict(re.findall(r"'((?:nav|footer|meta)\.[A-Za-z0-9_.]+)':\s*'((?:[^'\\]|\\.)*)'", esblk))
    def i18n(m):
        k = m.group(2)
        return m.group(1) + keys[k].replace("\\'", "'") + "<" if k in keys else m.group(0)
    body = re.sub(r'(data-i18n(?:-html)?="([^"]+)"[^>]*>)([^<]*)<', i18n, body)
    # hrefs localizados (data-i18n-href) resueltos en estático
    def ihref(m):
        k = m.group(2)
        return 'href="%s"%s' % (keys[k], m.group(3)) if k in keys else m.group(0)
    body = re.sub(r'href="([^"]*)"((?:\s+[a-z0-9-]+="[^"]*")*?\s+data-i18n-href="([^"]+)")', lambda m: ('href="%s"' % keys[m.group(3)] if m.group(3) in keys else 'href="%s"' % m.group(1)) + m.group(2), body)
    # assets con ruta absoluta (la página vive en /es/)
    for rel in ("styles.css", "script.js", "translations.js", "logo kinedu.png", "partner-logos/", "google-play-badge", "app-store-badge", "illustrations/", "fonts/"):
        body = body.replace('src="%s' % rel, 'src="/%s' % rel).replace('href="%s' % rel, 'href="/%s' % rel)
        head = head.replace('src="%s' % rel, 'src="/%s' % rel).replace('href="%s' % rel, 'href="/%s' % rel)
    html = head + body
    assert "—" not in re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S).replace("2020—2023", ""), "em dash en " + lang
    return html, missing

#!/usr/bin/env python3
"""Auditoria AEO (que agentes de IA como Meta Muse / ChatGPT / Bing Copilot puedan leer y
recomendar kinedu.com). Lista de 11 puntos (19-oct-2026) aplicada al sitio real.

Uso: python3 scripts/seo/aeo_audit.py            -> resumen en texto + JSON en
     ~/.config/kinedu-agent/history/aeo-AAAA-MM-DD.json (para comparar mes a mes)
El Medidor lo corre el primer lunes de cada mes y manda al backlog cualquier retroceso.
"""
import re, glob, json, os, html, datetime, urllib.request

HUBS = ['index.html','es/index.html','pt/index.html','masterclasses.html','es/masterclasses.html','pt/masterclasses.html',
        'science.html','es/science.html','pt/science.html','founder.html','book.html','es/book.html','pt/book.html',
        'gift.html','es/gift.html','pt/gift.html','experts.html','live-classes.html','es/live-classes.html','pt/live-classes.html']
EN_WORDS = re.compile(r"\b(the|your|what|with|every|today|baby's|for|and)\b", re.I)

def read(f):
    try: return open(f, encoding='utf-8', errors='ignore').read()
    except Exception: return None

def h1(s):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''

def audit():
    out = {'fecha': datetime.date.today().isoformat(), 'hubs': {}, 'blog': {}, 'robots': {}, 'resumen': {}}
    # 8) robots.txt: bots de IA permitidos?
    try:
        r = urllib.request.urlopen('https://www.kinedu.com/robots.txt', timeout=20).read().decode()
        blocked = [b for b in ('GPTBot','ClaudeBot','PerplexityBot','meta-webindexer','Meta-ExternalAgent','Bingbot','Google-Extended')
                   if re.search(rf'User-agent:\s*{re.escape(b)}\s*\n\s*Disallow:\s*/\s*$', r, re.I | re.M)]
        out['robots'] = {'bloqueados': blocked, 'ok': not blocked}
    except Exception as e:
        out['robots'] = {'error': str(e)[:80]}
    # 1, 2, 5, 7, 10, 11 en hubs
    for f in HUBS:
        s = read(f)
        if s is None: continue
        imgs = re.findall(r'<img\b[^>]*>', s)
        noalt = [i for i in imgs if not re.search(r'\balt="[^"]+"', i)]
        iconbtn = [b for b in re.findall(r'<button\b([^>]*)>(.*?)</button>', s, re.S)
                   if not re.sub(r'<[^>]+>', '', b[1]).strip() and 'aria-label' not in b[0]]
        inputs = len(re.findall(r'<(?:input|textarea|select)\b[^>]*>', s)); labels = len(re.findall(r'<label\b', s))
        t = h1(s); lang = 'es' if f.startswith('es/') else 'pt' if f.startswith('pt/') else 'en'
        raw_english = bool(lang != 'en' and t and EN_WORDS.search(t))
        out['hubs'][f] = {
            'img_sin_alt': len(noalt), 'img_total': len(imgs), 'botones_icono_sin_aria': len(iconbtn),
            'inputs': inputs, 'labels': labels, 'h1': t[:80], 'h1_en_ingles_siendo_es_pt': raw_english,
            'definicion': bool(re.search(r'Kinedu (is|es|é) (a|an|una|um|la|the) ', s)),
            'as_of': bool(re.search(r'\bas of 20\d\d|\ba 20\d\d\b|\bem 20\d\d\b', s, re.I)),
            'main': '<main' in s, 'header': '<header' in s, 'nav': '<nav' in s, 'footer': '<footer' in s,
            'dateModified': 'dateModified' in s, 'div_boton': len(re.findall(r'<div[^>]*(onclick=|role="button")', s)),
        }
    # blog: alt + fechas + H2-pregunta (muestra)
    for pat, lang in (('blog/*.html','en'), ('es/blog/*.html','es'), ('pt/blog/*.html','pt')):
        files = [x for x in sorted(glob.glob(pat)) if '/category/' not in x and '/stage/' not in x and 'preview-' not in x]
        tot = bad = nomod = q = n = 0
        for f in files:
            s = read(f) or ''; n += 1
            im = re.findall(r'<img\b[^>]*>', s); tot += len(im); bad += len([i for i in im if not re.search(r'\balt="[^"]+"', i)])
            if 'dateModified' not in s: nomod += 1
            m = re.search(r'<h2[^>]*>(.*?)</h2>', s, re.S)
            if m and '?' in re.sub(r'<[^>]+>', '', m.group(1)): q += 1
        out['blog'][lang] = {'posts': n, 'img_total': tot, 'img_sin_alt': bad, 'sin_dateModified': nomod, 'primer_h2_es_pregunta': q}
    hubs = out['hubs'].values()
    out['resumen'] = {
        'hubs_img_sin_alt': sum(h['img_sin_alt'] for h in hubs),
        'hubs_es_pt_con_h1_en_ingles': sum(1 for h in hubs if h['h1_en_ingles_siendo_es_pt']),
        'hubs_sin_definicion': sum(1 for h in hubs if not h['definicion']),
        'hubs_sin_as_of': sum(1 for h in hubs if not h['as_of']),
        'hubs_sin_main': sum(1 for h in hubs if not h['main']),
        'hubs_sin_dateModified': sum(1 for h in hubs if not h['dateModified']),
        'blog_img_sin_alt': sum(b['img_sin_alt'] for b in out['blog'].values()),
        'blog_img_total': sum(b['img_total'] for b in out['blog'].values()),
        'blog_primer_h2_pregunta': sum(b['primer_h2_es_pregunta'] for b in out['blog'].values()),
        'blog_posts': sum(b['posts'] for b in out['blog'].values()),
        'robots_ok': out['robots'].get('ok'),
    }
    return out

if __name__ == '__main__':
    o = audit(); r = o['resumen']
    print(f"AEO {o['fecha']} · hubs: {r['hubs_es_pt_con_h1_en_ingles']} ES/PT con H1 en ingles · {r['hubs_img_sin_alt']} img sin alt · "
          f"{r['hubs_sin_definicion']} sin definicion · {r['hubs_sin_as_of']} sin 'as of' · {r['hubs_sin_main']} sin <main> · {r['hubs_sin_dateModified']} sin dateModified · robots ok: {r['robots_ok']}")
    print(f"blog: {r['blog_img_sin_alt']}/{r['blog_img_total']} img sin alt · primer H2 es pregunta en {r['blog_primer_h2_pregunta']}/{r['blog_posts']} posts")
    d = os.path.expanduser('~/.config/kinedu-agent/history'); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"aeo-{o['fecha']}.json"); json.dump(o, open(p, 'w'), ensure_ascii=False, indent=1); print('json:', p)

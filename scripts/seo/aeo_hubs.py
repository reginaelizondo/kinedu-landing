#!/usr/bin/env python3
"""AEO en las páginas principales (aprobaciones 2026-10-21-2 y -4):

1. Alt descriptivo en los íconos de /science (estados y áreas, EN/ES/PT), en el ícono de
   la app y en la portada 3D del libro. No toca imágenes que ya traen alt.
2. HTML semántico: envuelve la barra de navegación en <header> y el contenido entre la
   barra y el <footer> en <main>, en los hubs que no lo tienen (book ya lo traía).
3. Frescura en las 9 páginas de /science: schema WebPage con datePublished/dateModified
   (última fecha de cambio de contenido según git) y línea visible "Updated on …".

Idempotente: correrlo dos veces no duplica nada. Uso: python3 scripts/seo/aeo_hubs.py [--dry]
"""
import re, os, sys, json, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
DRY = "--dry" in sys.argv

HUBS = ['index.html', 'es/index.html', 'pt/index.html', 'masterclasses.html', 'es/masterclasses.html', 'pt/masterclasses.html',
        'science.html', 'es/science.html', 'pt/science.html', 'founder.html', 'book.html', 'es/book.html', 'pt/book.html',
        'gift.html', 'es/gift.html', 'pt/gift.html', 'experts.html', 'live-classes.html', 'es/live-classes.html', 'pt/live-classes.html',
        'science-what-we-know.html', 'es/science-what-we-know.html', 'pt/science-what-we-know.html',
        'science-what-you-can-do.html', 'es/science-what-you-can-do.html', 'pt/science-what-you-can-do.html']
SCIENCE = [h for h in HUBS if 'science' in h]

ALT = {
    'en': {
        'states/upcoming': 'Upcoming: a skill that usually develops at a later age',
        'states/reinforce': 'Reinforce: a skill expected around this age and still developing',
        'states/ontrack': 'On track: a skill showing at the expected age',
        'states/mastered': 'Mastered: a skill showing consistently',
        'areas/physical': 'Physical development area icon',
        'areas/cognitive': 'Cognitive development area icon',
        'areas/linguistic': 'Language development area icon',
        'areas/emotional': 'Social-emotional development area icon',
        'app/icon': 'Kinedu app icon',
        'book/cover-3d-sm-v2': 'Big Bang Baby, the book by Kinedu founder Luis Garza Sada',
    },
    'es': {
        'states/upcoming': 'En camino: habilidad que suele desarrollarse a una edad posterior',
        'states/reinforce': 'Reforzar: habilidad esperada alrededor de esta edad, todavía en desarrollo',
        'states/ontrack': 'Adquiridas: habilidad que se muestra a la edad esperada',
        'states/mastered': 'Sobresaliente: habilidad que se muestra de forma consistente',
        'areas/physical': 'Ícono del área de desarrollo físico',
        'areas/cognitive': 'Ícono del área de desarrollo cognitivo',
        'areas/linguistic': 'Ícono del área de desarrollo del lenguaje',
        'areas/emotional': 'Ícono del área de desarrollo socioemocional',
        'app/icon': 'Ícono de la app Kinedu',
        'book/cover-3d-sm-v2': 'Big Bang Baby, el libro de Luis Garza Sada, fundador de Kinedu',
    },
    'pt': {
        'states/upcoming': 'A caminho: habilidade que costuma se desenvolver em uma idade posterior',
        'states/reinforce': 'Reforçar: habilidade esperada por volta desta idade, ainda em desenvolvimento',
        'states/ontrack': 'Adquiridas: habilidade que aparece na idade esperada',
        'states/mastered': 'Excelente: habilidade que aparece de forma consistente',
        'areas/physical': 'Ícone da área de desenvolvimento físico',
        'areas/cognitive': 'Ícone da área de desenvolvimento cognitivo',
        'areas/linguistic': 'Ícone da área de desenvolvimento da linguagem',
        'areas/emotional': 'Ícone da área de desenvolvimento socioemocional',
        'app/icon': 'Ícone do app Kinedu',
        'book/cover-3d-sm-v2': 'Big Bang Baby, o livro de Luis Garza Sada, fundador do Kinedu',
    },
}
UPDATED = {'en': 'Updated on {d}', 'es': 'Actualizado el {d}', 'pt': 'Atualizado em {d}'}
MONTHS = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'es': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
    'pt': ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'],
}
NOISE = ('Bump script.js', 'Metatags de preview', 'translations', 'Google Fonts', 'AEO:')

def lang_of(f):
    return 'es' if f.startswith('es/') else 'pt' if f.startswith('pt/') else 'en'

def fmt(d, lang):
    y, m, dd = d.split('-')
    m = MONTHS[lang][int(m) - 1]
    return {'en': f'{m} {int(dd)}, {y}', 'es': f'{int(dd)} de {m} de {y}', 'pt': f'{int(dd)} de {m} de {y}'}[lang]

def git_dates(f):
    log = subprocess.run(['git', 'log', '--format=%ad %s', '--date=short', '--', f], capture_output=True, text=True).stdout.splitlines()
    content = [l for l in log if not any(n in l for n in NOISE)] or log
    return log[-1][:10], content[0][:10]  # (primer commit, último cambio de contenido)

report = []
for f in HUBS:
    s = open(f, encoding='utf-8').read(); orig = s; lang = lang_of(f); notes = []

    # 1) alt en imágenes con alt="" conocidas
    def fix_alt(m):
        tag = m.group(0)
        src = re.search(r'src="/images/([^"]+)\.(?:png|webp|jpg)"', tag)
        if not src: return tag
        key = src.group(1)
        if key in ALT[lang]:
            notes.append('alt ' + key)
            return tag.replace('alt=""', 'alt="' + ALT[lang][key] + '"', 1)
        return tag
    s = re.sub(r'<img\b[^>]*\balt=""[^>]*>', fix_alt, s)
    # ícono de área que arma el JS de la pregunta de muestra: usa el nombre del área
    js_old = """'<img src="/images/areas/' + q.icon + '.png" alt="" width="30" height="30" style="display:block">'"""
    js_new = """'<img src="/images/areas/' + q.icon + '.png" alt="' + q.area + '" width="30" height="30" style="display:block">'"""
    if js_old in s:
        s = s.replace(js_old, js_new); notes.append('alt js q.area')

    # 2) <header> alrededor de la barra y <main> alrededor del contenido
    if '<main' not in s:
        nav_start = s.find('<nav class="navbar"')
        nav_end = s.find('</nav>', nav_start) + len('</nav>')
        foot = s.find('<footer', nav_end)
        assert nav_start > 0 and foot > nav_end, f + ': no encuentro navbar/footer'
        s = (s[:nav_start] + '<header>\n' + s[nav_start:nav_end] + '\n</header>\n<main>' +
             s[nav_end:foot] + '</main>\n' + s[foot:])
        notes.append('header+main')
    elif '<header' not in s:
        nav_start = s.find('<nav class="navbar"')
        nav_end = s.find('</nav>', nav_start) + len('</nav>')
        s = s[:nav_start] + '<header>\n' + s[nav_start:nav_end] + '\n</header>' + s[nav_end:]
        notes.append('header')

    # 3) frescura en /science: schema WebPage + línea visible
    if f in SCIENCE and 'dateModified' not in s:
        first, last = git_dates(f)
        title = re.search(r'<title>([^<]*)</title>', s).group(1).strip()
        canon = re.search(r'<link rel="canonical" href="([^"]*)"', s)
        url = canon.group(1) if canon else 'https://www.kinedu.com/' + f.replace('.html', '').replace('index', '')
        wp = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url, "inLanguage": lang,
              "datePublished": first, "dateModified": last,
              "publisher": {"@type": "Organization", "name": "Kinedu", "url": "https://www.kinedu.com"}}
        s = s.replace('</head>', '<script type="application/ld+json">' + json.dumps(wp, ensure_ascii=False) + '</script>\n</head>', 1)
        line = f'<p class="sci-updated" style="margin-top:14px;font-size:13px;color:#8A94A8">{UPDATED[lang].format(d=fmt(last, lang))}</p>'
        m = re.search(r'<p class="hero-sub">.*?</p>', s, re.S)
        assert m, f + ': sin hero-sub'
        s = s[:m.end()] + '\n            ' + line + s[m.end():]
        notes.append(f'dateModified {last} (publicado {first})')

    if s != orig:
        report.append((f, notes))
        if not DRY:
            open(f, 'w', encoding='utf-8').write(s)

for f, notes in report:
    print(f, '·', ', '.join(notes))
print(('(dry) ' if DRY else '') + f'{len(report)} archivos')

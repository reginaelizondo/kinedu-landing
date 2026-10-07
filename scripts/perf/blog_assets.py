#!/usr/bin/env python3
"""Peso de los posts del blog (recomendación 3 del Estratega, 6-oct-2026):
- Google Fonts: de 6 archivos de Plus Jakarta Sans a solo la itálica (Proxima Nova,
  self-hosted, es la que pinta; no tiene cara itálica).
- translations.js (121 KB, tres idiomas) -> translations-<lang>.js (~40 KB) según la
  carpeta del post. script.js carga otro idioma bajo demanda si hace falta.
Idempotente. Correr también en posts nuevos. Solo archivos rastreados por git."""
import os, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = "1007a"
FONT_OLD = re.compile(r'href="https://fonts\.googleapis\.com/css2\?family=Plus\+Jakarta\+Sans:[^"]*"')
FONT_NEW = 'href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital@1&display=swap"'
TR_OLD = re.compile(r'<script src="/translations(?:-(?:en|es|pt))?\.js\?v=[0-9a-z]+" defer>')
SC_OLD = re.compile(r'<script src="/script\.js\?v=[0-9a-z]+" defer>')

files = subprocess.run(["git", "ls-files", "blog", "es/blog", "pt/blog"], cwd=ROOT, capture_output=True, text=True).stdout.split()
n = 0
for rel in files:
    if not rel.endswith(".html"): continue
    lang = rel.split("/")[0] if rel.startswith(("es/", "pt/")) else "en"
    fp = os.path.join(ROOT, rel)
    h = open(fp, encoding="utf-8").read(); o = h
    h = FONT_OLD.sub(FONT_NEW, h)
    if TR_OLD.search(h):
        h = TR_OLD.sub('<script src="/translations-%s.js?v=%s" defer>' % (lang, V), h)
        h = SC_OLD.sub('<script src="/script.js?v=%s" defer>' % V, h)
    if h != o:
        open(fp, "w", encoding="utf-8").write(h); n += 1
print("posts actualizados:", n)

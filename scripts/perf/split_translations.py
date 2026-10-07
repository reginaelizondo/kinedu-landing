#!/usr/bin/env python3
"""Parte translations.js (los tres idiomas, ~121 KB) en translations-en.js,
translations-es.js y translations-pt.js para que cada página cargue solo el
idioma de su carpeta. translations.js completo se queda para las páginas que
necesitan los tres idiomas a la vez (home, live classes, etc.).

Cada archivo hace Object.assign sobre window.TRANSLATIONS, así que pueden
convivir y script.js carga el que falte bajo demanda (ver applyTranslations).
Correr después de cualquier cambio en translations.js."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(ROOT, "translations.js"), encoding="utf-8").read()
lines = src.split("\n")
starts = {}
for i, l in enumerate(lines):
    m = re.match(r"^  (en|es|pt): \{\s*$", l)
    if m: starts[m.group(1)] = i
assert len(starts) == 3, starts
order = sorted(starts, key=starts.get)
ends = {}
for n, lang in enumerate(order):
    stop = starts[order[n + 1]] if n + 1 < len(order) else len(lines)
    # el bloque cierra en la última línea "  }," o "  }" antes del siguiente idioma / del final
    for j in range(stop - 1, starts[lang], -1):
        if re.match(r"^  \},?\s*$", lines[j]): ends[lang] = j; break
    assert lang in ends, lang
out = []
for lang in order:
    body = lines[starts[lang]:ends[lang] + 1]
    body[-1] = "  }"
    js = ("/* Generado por scripts/perf/split_translations.py a partir de translations.js. No editar a mano. */\n"
          "window.TRANSLATIONS = Object.assign(window.TRANSLATIONS || {}, {\n" + "\n".join(body) + "\n});\n")
    fp = os.path.join(ROOT, "translations-%s.js" % lang)
    open(fp, "w", encoding="utf-8").write(js)
    out.append("%s: %d KB" % (os.path.basename(fp), len(js.encode("utf-8")) // 1024))
print("translations.js: %d KB ->" % (len(src.encode("utf-8")) // 1024), ", ".join(out))

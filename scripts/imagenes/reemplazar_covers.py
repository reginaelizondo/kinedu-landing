"""Reemplaza fotos de stock del blog por fotos licenciadas de blog-photos/.

Uso: python3 scripts/imagenes/reemplazar_covers.py scripts/imagenes/ENVATO_LOTE_2.md [--apply]
Lee la tabla del lote (columnas "Guardar como" y "Reemplaza a"). Las filas cuya
foto todavía no está en blog-photos/ se saltan, así que se puede correr con un
lote a medio descargar. Sin --apply solo simula."""
import csv, datetime, os, re, sys
from collections import Counter

DRY = "--apply" not in sys.argv
LOTE = next(a for a in sys.argv[1:] if not a.startswith("--"))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)

mapping = {}
for line in open(LOTE, encoding="utf-8"):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 4 and cells[2].endswith(".jpg"):
        photo = cells[2][:-4]
        if os.path.exists(f"blog-photos/{photo}.jpg"):
            mapping[photo] = cells[3]
        else:
            print("falta descargar:", cells[2])
assert len(set(mapping.values())) == len(mapping), "target repetido"
lote_n = re.search(r"(\d+)", os.path.basename(LOTE)).group(1)

def target_re(t):
    m = re.match(r"(shutterstock|istock|getty)_(\d+)$", t)
    if m:
        core = rf"{m.group(1)}[_-]?0*{m.group(2)}(?!\d)"
    else:
        core = re.escape(t) + r"(?:-\d+x\d+)?(?=\.)"
    return re.compile(r"(?:https://www\.kinedu\.com)?/blog-media/[^\"'\s)>]*?" + core + r"[^\"'\s)>]*?\.(jpe?g|png|gif|webp)", re.I)

def file_re(t):
    m = re.match(r"(shutterstock|istock|getty)_(\d+)$", t)
    if m:
        return re.compile(rf"{m.group(1)}[_-]?0*{m.group(2)}(?!\d)", re.I)
    return re.compile(r"^" + re.escape(t) + r"(?:-\d+x\d+)?\.", re.I)

targets = {t: (photo, target_re(t)) for photo, t in mapping.items()}

pages = []
for folder, dirs, files in os.walk("."):
    if folder.startswith(("./.git", "./blog-media", "./blog-photos", "./node_modules")):
        dirs[:] = []
        continue
    for fn in files:
        if fn.endswith((".html", ".xml", ".json")):
            pages.append(os.path.join(folder, fn)[2:])

IMG_TAG = re.compile(r"<img\b[^>]*>")
touched_pages = 0
refs = Counter()
for p in pages:
    s = open(p, encoding="utf-8").read()
    orig = s
    for t, (photo, rx) in targets.items():
        def repl(m, photo=photo):
            ext = "webp" if m.group(1).lower() == "webp" else "jpg"
            prefix = "https://www.kinedu.com" if m.group(0).startswith("https://") else ""
            refs[t] += 1
            return f"{prefix}/blog-media/covers/{photo}.{ext}"
        s = rx.sub(repl, s)
    if s != orig:
        def fix_dims(m):
            tag = m.group(0)
            if "/blog-media/covers/" not in tag:
                return tag
            tag = re.sub(r'\bwidth="\d+"', 'width="1200"', tag)
            tag = re.sub(r'\bheight="\d+"', 'height="800"', tag)
            return tag
        s = IMG_TAG.sub(fix_dims, s)
        if 'og:image" content="https://www.kinedu.com/blog-media/covers/' in s:
            s = re.sub(r'(property="og:image:width"\s+content=")\d+', r"\g<1>1200", s)
            s = re.sub(r'(property="og:image:height"\s+content=")\d+', r"\g<1>800", s)
        touched_pages += 1
        if not DRY:
            open(p, "w", encoding="utf-8").write(s)

old_files = []
for folder, dirs, files in os.walk("blog-media"):
    if folder.startswith("blog-media/covers"):
        continue
    for fn in files:
        for t in targets:
            if file_re(t).search(fn):
                old_files.append(os.path.join(folder, fn))
                break

missing = [t for t in targets if refs[t] == 0]
print("modo:", "DRY RUN" if DRY else "APPLY")
print("páginas modificadas:", touched_pages)
print("referencias reemplazadas:", sum(refs.values()))
print("archivos viejos a borrar:", len(old_files))
print("targets sin referencias:", missing)

if not DRY:
    from PIL import Image, ImageOps
    os.makedirs("blog-media/covers", exist_ok=True)
    for photo in mapping:
        im = ImageOps.exif_transpose(Image.open(f"blog-photos/{photo}.jpg")).convert("RGB")
        im = ImageOps.fit(im, (1200, 800), Image.LANCZOS, centering=(0.5, 0.45))
        im.save(f"blog-media/covers/{photo}.jpg", quality=82, optimize=True, progressive=True)
        im.save(f"blog-media/covers/{photo}.webp", quality=80, method=6)
    for f in old_files:
        os.remove(f)
    hoy = datetime.date.today().isoformat()
    with open("scripts/imagenes/registro-covers.csv", "a", newline="") as fh:
        w = csv.writer(fh)
        for photo, old in mapping.items():
            w.writerow([f"blog-media/covers/{photo}.webp", "Envato Elements (suscripción Kinedu)",
                        f"blog-photos/{photo}.jpg", old, lote_n, hoy])
    print("covers generadas, archivos viejos borrados y registro actualizado")

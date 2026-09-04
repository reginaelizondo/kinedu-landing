# Genera es/index.html y pt/index.html a partir de index.html: rutas absolutas + <title>/description/OG localizados + lang.
import re,json,os
L="/Users/reginaelizondo/Desktop/CLAUDE/Landing Page"
src=open(L+"/index.html",encoding="utf-8").read()
tr=open(L+"/translations.js",encoding="utf-8").read()
def val(lang,key):
    m=re.search(r'\b%s:\s*\{'%lang,tr); seg=tr[m.end():]
    mm=re.search(r"'%s':\s*'((?:[^'\\]|\\.)*)'"%re.escape(key),seg); return mm.group(1).replace("\\'","'") if mm else None
for lang in ("es","pt"):
    s=src
    # rutas relativas → absolutas (src/href/srcset que no empiecen con http, /, #, mailto, data:)
    s=re.sub(r'\b(src|href|srcset|poster)="(?!https?:|/|#|mailto:|tel:|data:|javascript:)([^"]+)"', lambda m: '%s="/%s"'%(m.group(1),m.group(2)), s)
    s=re.sub(r"url\('(?!https?:|/|data:)([^']+)'\)", r"url('/\1')", s)
    s=s.replace('<html lang="en"','<html lang="%s"'%lang,1)
    t=val(lang,'meta.title'); d=val(lang,'meta.description') or val(lang,'hero.sub') or val(lang,'hero.subtitle')
    if d: d=re.sub(r'<[^>]+>','',d).replace('\\n',' ').strip()
    if t: s=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%t,s,1); s=re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>'+t, s); s=re.sub(r'(<meta name="twitter:title" content=")[^"]*', r'\g<1>'+t, s)
    if d: s=re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>'+d, s); s=re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>'+d, s); s=re.sub(r'(<meta name="twitter:description" content=")[^"]*', r'\g<1>'+d, s)
    s=re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>https://www.kinedu.com/%s'%lang, s)
    s=re.sub(r'(<link rel="canonical" href=")[^"]*', r'\g<1>https://www.kinedu.com/%s'%lang, s)
    s=s.replace('<meta property="og:locale" content="en_US">','<meta property="og:locale" content="%s">'%('es_MX' if lang=='es' else 'pt_BR'))
    s='<!-- GENERADO desde index.html por scripts/build-home-locales (no editar a mano): solo cambia <head> localizado y rutas absolutas -->\n'+s
    os.makedirs(L+"/"+lang,exist_ok=True); open(L+"/%s/index.html"%lang,"w",encoding="utf-8").write(s)
    print(lang,"→",lang+"/index.html", "title:",t, "| desc:",(d or "")[:50])

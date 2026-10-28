# Bitácora de Marina

Registro único de lo que hace el agente de la landing. Generado desde `bitacora.jsonl` (no editar a mano; usar `scripts/agent/bitacora.py`).

Última actualización: 2026-10-28 10:16.


## Semana del 2026-10-26

- 🔧 **2026-10-28-01** · Contenido · Preview EN: hub 'Oral phase in babies' que consolida oral-stage-of-development + 2 posts de mouthing (consolida de Regina 8-oct)  _(Implementador)_
  - _estado: preview · commit 11e10a309 · medir: 2026-11-25 · ⏳ por medir_
  - Se queda /blog/oral-stage-of-development (28 clics, pos 7.4, racimo 'oral phase baby'); why-do-babies-put-everything-in-their-mouths (3 clics, pos 16) y mouthing-why-does-everything-end-up-in-my-babys-mouth (3 clics, pos 18) iran con 301 al 'va'. Reescritura completa: 1,927 palabras, 10 H2 (primer H2 = la pregunta del lector con respuesta de 97 palabras), tabla por edad, teething vs mouthing, seguridad, que hacer si traga algo, FAQ de 7 con schema; CTA masterclass de primeros auxilios y app (sensory play). Noindex, sin enlazar, fuera del sitemap. Esperado: capturar 'oral phase baby' + 'why do babies put everything in their mouth' en una sola URL; se mide en GSC 4 semanas despues de publicar.
- 🔧 **2026-10-28-02** · SEO · AEO hubs: <header>/<main> en 26 paginas principales, alt en iconos de science/app/libro, dateModified + 'Updated on' en las 9 de science  _(Implementador)_
  - _estado: publicado · commit a1de88a3c · medir: 2026-11-20 · ⏳ por medir_
  - Aprobaciones 2026-10-21-2 (parte science) y -4. Auditoria AEO: hubs sin <main> 16 a 0, img sin alt en hubs 96 a 54 (quedan el pixel de Meta y fotos de live-classes), hubs sin dateModified 17 a 14. Fecha visible = ultimo cambio real de contenido segun git (30-sep-2026), no la de hoy. Script idempotente scripts/seo/aeo_hubs.py. Sin efecto visible salvo la linea 'Updated on' en science. Pendiente: alt masivo del blog (3,830 img) y definicion/as-of visibles del home, que esperan el A/B del hero (~10-nov).

## Semana del 2026-10-19

- 🔧 **2026-10-20-01** · Gift · Llegada real al checkout de Gift (checkout_viewed) en Web Promos  _(Claude)_
  - _estado: publicado · commit ac1c0c3 · medir: 2026-10-27 · ⏳ por medir_
  - POST /api/gift/view al abrir /gift/checkout (una por pestana, mismo session_id gift-<vid> que funnel_started); admin-summary lo cuenta unico por sesion y dia. Antes solo existia funnel_started, que se dispara al ENVIAR el formulario, asi que el embudo decia 'llegaron' cuando media 'iniciaron el pago'. Verificado en prod con env=qa: 2 llegadas misma sesion = 1. Pedido del 7-oct, va de Regina 20-oct. Esperado: ver por fin donde se cae la gente entre el clic en /gift y el pago.
- 🔧 **2026-10-20-02** · Gift · /analytics Gift: 'Llegaron al checkout' pasa a ser la llegada real y el envio del formulario se llama 'Iniciaron el pago (Stripe)'  _(Claude)_
  - _estado: publicado · commit 32beeca5b · medir: 2026-10-27 · ⏳ por medir_
  - Embudo y serie diaria separan llegada (checkout_viewed) de inicio de pago (checkout_started). El paso 'Llegaron' solo aparece cuando Web Promos ya manda el dato.
- 💡 **2026-10-20-03** · A/B · Prueba de lectura obligatoria antes de publicar un A/B: mandar un ab_view y un c  _(Marina)_
- 🔧 **2026-10-20-04** · A/B · A/B menu movil: arreglo de medicion (ab_view/ab_cta con variante menu-a|b)  _(Claude)_
  - _estado: publicado · commit 628c72bd4 · medir: 2026-11-03 · ⏳ por medir_
  - Desde el 16-oct el test estaba ciego por dos huecos: mandaba menu_open/menu_click (no existen en /api/track, caian como pageview) y el listener del clic estaba en burbuja mientras script.js hace stopPropagation en el <a>. Ahora abre=ab_view, clic=ab_cta (evento nuevo que no suma conversiones), variante menu-a|b -> abSummary.menu. Verificado en local. Contar las 1,000 aperturas por variante desde el 20-oct.
- 🔧 **2026-10-20-05** · A/B · CTAs del blog: B fija para todos (A/B cerrado, gano B +180%)  _(Claude)_
  - _estado: publicado · commit 392eca26f · medir: 2026-11-03 · ⏳ por medir_
  - Aprobado con boton por Regina 20-oct (propuesta 2026-10-20-1). 3,416 posts: siempre B, sin sorteo ni persistencia, ?blogcta=a como escape de QA; se apaga ab_view y la conversion sin variante para congelar la tarjeta A/B. Esperado: clics al CTA del blog ~1.6% sostenido; vigilar correos y pagadas de landing-kinedu en Web Promos 2 semanas (un clic no es una venta).
- • **2026-10-20-06** · SEO · Search Console limpio: sin acciones manuales ni problemas de seguridad (verificado por Regina 20-oct)  _(Claude)_
  - Las dos pantallas de Seguridad y Acciones manuales dicen 'No se ha detectado ningun problema'. Queda descartada la penalizacion manual: la caida desde el 2-3 oct es algoritmica (update de calidad), consistente con la inspeccion de URL (30 top losers indexadas y rastreadas). El plan sigue: leer la semana 20-26 el lunes 27, luego series plantilla y autor experto.
- • **2026-10-20-07** · Gift · In-app Gift iOS: goal corregido a CreateUserGift_Web 7d; resultado real 469 vistas, 0 regalos (14-20 oct)  _(Claude)_
  - Regina cambio el conversion event en CleverTap (antes PPPaymentSuccess a 5 minutos). CTR 97% sigue inflado porque nuestra X es un <a href=wzrk://dismiss> y CleverTap la cuenta como clic (su aviso excluye solo su boton nativo). Clic real = llegadas a /gift con utm_source=inapp en /analytics. Siguiente: audiencia con intencion (visito /gift, baby shower) en vez de todos los Premium learn, tope de frecuencia, y X sin <a href> en el generador scripts/iam/build_gift_iam.py. Ojo: banner de CleverTap 123% del plan (overage facturado).
- • **2026-10-20-08** · SEO · Bing Webmaster Tools ya estaba dado de alta y verificado (www.kinedu.com): 818 clics / 123.3K impresiones en ~6 semanas, SIN caida en octubre  _(Claude)_
  - Confirmado por Regina 20-oct en el panel de Bing. La grafica se mantiene plana hasta el 11-oct: la caida es exclusiva de Google. Tareas: (1) Medidor conecta la API de Bing al weekly_pull (Regina genera la API key en Bing WMT > Settings > API access y la pone como BING_API_KEY en ~/.config/kinedu-agent/.env); (2) implementar IndexNow (clave en raiz + ping al publicar), recomendacion del propio Bing; (3) ignorar el aviso de meta descriptions cortas (son cortas a proposito).
- • **2026-10-21-01** · SEO · Auditoria AEO 21-oct (lista de 11 puntos de Meta Muse): 2 cumplidos, 5 fallan, propuestos con boton  _(Claude)_
  - Cumplidos: robots.txt abierto a bots de IA; testimonios en texto. Fallan: (1) /es y /pt sirven ingles en el HTML crudo y traducen con JS; (2) ~15% de imagenes del blog sin alt y science.html 14/16; (3) sin definicion 'Kinedu es...' ni 'as of' en claims; (4) sin <main>/<header> ni dateModified en hubs; (5) no hay paginas comparativas 'Kinedu vs'. Propuestas 2026-10-21-1..5 en Slack.
- 🔧 **2026-10-21-02** · SEO · AEO: definicion de Kinedu (schema MobileApplication) en HTML crudo EN/ES/PT + dateModified en /book  _(Claude)_
  - _estado: publicado · commit ebaab73ac · medir: 2026-11-20 · ⏳ por medir_
  - Parte de las aprobaciones 2026-10-21-3 y -4. Definicion que es/para quien/que hace, con rating 4.7 y audiencia, legible por crawlers de IA sin ejecutar JS, en los 3 idiomas. Esperado: mejor descripcion cuando ChatGPT/Perplexity/Muse nos citen (prueba de citacion mensual del Investigador). No toca hero (A/B) ni blog (freeze).
- 🔧 **2026-10-21-03** · Infra · Bing Webmaster Tools conectado al pull semanal del agente  _(Claude)_
  - _estado: publicado · commit a3512a789 · medir: 2026-10-27 · ⏳ por medir_
  - Regina genero la BING_API_KEY en Bing WMT y quedo en ~/.config/kinedu-agent/.env. weekly_pull.py ahora trae out['bing'] (clics/impresiones 28d vs 28d, serie diaria) via GetRankAndTrafficStats, junto a Google. Primer dato: 28d 524 clics / 77,634 impr. Sirve de contraste: Bing no tuvo la caida de Google (la caida es exclusiva de Google). 'AI Performance' de Bing aun sin API publica, se revisa a mano.
- • **2026-10-22-01** · SEO · Investigacion comparativas AEO: las paginas 'Kinedu vs' NO tienen demanda; si la tienen 'best baby development apps' (con prompts de IA en GSC) y 'kinedu reviews'  _(Claude)_
  - GSC 90d: 'baby sparks vs kinedu' 2 impresiones. En cambio salen prompts estilo ChatGPT rankeando pos 2-3 ('compare the best baby development apps?', 'best app for evidence-based parenting') y rankeamos bien en 'best baby milestone app' (pos 1). Y 'kinedu reviews'/'kinedu app review' ~1,100 impr pos 1.8-2.1 con solo ~12 clics (CTR 1.2%): no tenemos pagina de resenas propia. Plan: roundup 'Best baby development apps 2026' (H2-pregunta + depende + tabla por caso de uso) y pagina de reviews. Publicar tras el freeze. Orden de trabajo en 05-investigador/comparativas-aeo-2026-10-22.md.
- • **2026-10-22-02** · SEO · Aviso GSC 'Pagina con redireccion' = efecto esperado de nuestros 301, no es problema  _(Claude)_
  - Correo de Search Console 22-oct sobre paginas de sitemap no indexadas por 'Pagina con redireccion'. Verificado: son las URLs viejas que consolidamos con 301 (mollera, moleira, primavera, sono 8 meses PT) entre el 8 y 16 oct; Google indexa el destino, no la que redirige, que es lo correcto. El sitemap (3,489 URLs) solo tiene destinos; muestra de 40 URLs del sitemap = 40 dan 200, ninguna redirige. No es parte de la caida (esa es algoritmica). Opcional: 'Validar correccion' en el informe para que Google las saque del aviso. Nada que arreglar.
- 💡 **2026-10-22-03** · SEO · Correo GSC 'Pagina con redireccion' = nuestros 301, no problema: como verificar y reportar  _(Marina)_
  - Regla subida tras el correo de GSC del 22-oct que Regina reviso. Verificar sitemap solo-destinos + muestra 40 URLs todas 200 + cruzar con vercel.json antes de alarmar. Ver ROL del Guardia para el protocolo de correos de Search Console.

## Semana del 2026-10-12

- 🔧 **2026-10-12-01** · Contenido · 3 piezas del 9-oct construidas como preview  _(Implementador)_
  - _estado: preview · commit f46612795 · ⏳ por medir_
  - recién nacido ES (reescritura parcial + FAQ), atividades maternal PT (7 H2), hub de sueño PT. Noindex, sin enlazar. Regina dio 'va' el 12-oct.
- ⚠️ **2026-10-12-02** · SEO · Caída fuerte de tráfico Google semana 3-9 oct (-49.7%)  _(Medidor)_
  - Blog 1,644→692 clics. Empieza 2-3 oct, ANTES del retítulo del 7. Coincide con el September 2026 Spam Update. El 28d lo esconde. Congelar cambios masivos de plantilla.
- ⚠️ **2026-10-12-03** · A/B · A/B hero móvil no se puede leer (0 clics)  _(Medidor)_
  - _estado: pendiente_
  - El beacon del home solo escucha enlaces a app.kinedu.com; el hero va a webpromo. Tarea al Implementador: mandar conversion con variant al clic del hero y badges.
- 🔧 **2026-10-12-04** · Gift · In-App Message de Gift para premium (CleverTap) entregado  _(Claude)_
  - _estado: publicado · medir: 2026-11-15 · ⏳ por medir_
  - IAM full-screen EN/ES/PT con brand book, botón al web /gift con utm (inapp/iam/gift-premium) para trackear llegadas y ventas en /analytics. Escala a la caja de CleverTap.
  - **Resultado:** Publicadas el 15-oct con va de Regina (commit nuevo)
- 🔧 **2026-10-12-05** · Proceso · Bitácora de Marina creada  _(Claude)_
  - _estado: publicado · medir: 2026-10-19 · ✅ win_
  - Fuente única bitacora.jsonl + script bitacora.py (add/set/aprende/report) + tablero HTML en ~/Downloads/Marina-Avance. Enganchada a los roles: Implementador anota cada cambio, Medidor lo cierra con resultado+impacto y pega el avance en Slack los lunes.
  - **Resultado:** Sistema funcionando; 12 entradas y 7 aprendizajes sembrados del historial.
- ⚠️ **2026-10-12-06** · Conversión · Conversiones del 12-oct caen 65% con tráfico normal  _(Guardia)_
  - _medir: 2026-10-14_
  - Lunes 12-oct: 9 conversiones contra 34 el lunes 5 y promedio 26 en 7 días; domingo 11 con 8. Visitas 724, únicos 298, home 244 vistas (normal). Badges del hero 5 clics contra 15. Beacons vivos en el HTML, /api/track 200, sin cambios de código desde 7-oct. Clarity: rage clicks 46 contra 14 a 19 (29 de 3 sesiones en dos posts ES con muchas imágenes), errores de script 17 normal. Avisado en Slack ts 1791858898.201179. Si martes y miércoles siguen bajo 15, revisar llegada de eventos conversion a Supabase.
- 🔧 **2026-10-15-01** · Gift · Landing /gift mejorada: CTA naranja + confianza + sticky móvil (EN/ES/PT)  _(Claude)_
  - _estado: publicado · commit 30a812d18 · medir: 2026-10-22 · ⏳ por medir_
  - Tras ver 25 grabaciones de Clarity del in-app: CTA naranja 'Gift Kinedu now' en hero/planes/cierre, línea de confianza bajo el CTA (un solo pago · no se les cobra · no se renueva), CTA pegado en móvil, pulido móvil (menos hueco, chips, text-wrap:balance). Objetivo: que se queden y piquen.
- 📊 **2026-10-15-02** · Gift · Insight Clarity in-app: rebote alto + fuga en el checkout de webpromo  _(Claude)_
  - De 162 'clics' del in-app solo ~28 sesiones reales en /gift; dos grupos: rebotan en segundos (premium sin intención de regalar) y los que leen no pican o abandonan en el checkout de webpromo (la fuga grande, fuera de este repo). Orgánico engancha 30s vs 1.5s del in-app. Resumen IA de Clarity apunta a optimizar checkout + enganche inicial + audiencia.
- 💡 **2026-10-15-03** · Gift · Para el checkout de Gift medir y bajar fricción en webpromo (es donde muere la i  _(Marina)_
- 🔧 **2026-10-15-04** · A/B · Fix tracking A/B hero móvil (el botón iba a webpromo, no se medía)  _(Claude)_
  - _estado: publicado · commit 6f5d31b90 · medir: 2026-10-29 · ⏳ por medir_
  - Hero medido aparte con variante; ab_view solo si localStorage ok; badges con variante. Las 1,000 vistas/variante cuentan desde hoy.
- 🔧 **2026-10-15-05** · SEO · Fuera guiones largos del copy de plantilla del blog (3,418 posts)  _(Claude)_
  - _estado: publicado · commit edb9f2a49 · ✅ win_
  - Regla dura del jefe; coma en slim CTA/app CTA/footer EN-ES-PT, sin tocar cuerpo ni etiquetas de analytics.
  - **Resultado:** 0 guiones de plantilla restantes
- 🔧 **2026-10-16-01** · Landing · Clics muertos del hero a clic útil (título + imagen, móvil)  _(Claude)_
  - _estado: publicado · medir: 2026-10-29 · ⏳ por medir_
  - Heatmap Clarity: en móvil tocan el titular y la imagen del teléfono sin que hagan nada; ahora mandan al free trial, medidos como 'Hero — Visual tap' con variante.
- 🔧 **2026-10-16-02** · SEO · 301 de la única URL 404 con tráfico (sueño 8 meses PT)  _(Claude)_
  - _estado: publicado · commit 5706d1f06 · ✅ win_
  - De 1,000 páginas con tráfico GSC solo 1 rota (slug viejo do-sono rankeando #1); 301 a la viva de-sono. Las otras ~55 sin tráfico se dejan 404.
  - **Resultado:** Recupera #1 + 2 clics/50 impr
- 🔧 **2026-10-16-03** · A/B · A/B menú móvil del home (B = por secciones, acciones arriba)  _(Claude)_
  - _estado: publicado · commit 2e950e465 · medir: 2026-11-02 · ⏳ por medir_
  - Heatmap: hamburguesa #1 y ~46% abre y cierra sin elegir. B reconstruye el menú en EMPIEZA/EXPLORA/MÁS reusando links traducidos, solo móvil, sin tocar desktop. Mide menu_open/menu_click con variante. Verificado EN/ES/PT.

## Semana del 2026-10-05

- 🔧 **2026-10-06-01** · Landing · Contact us pasa de mailto a formulario con tracking  _(Claude)_
  - _estado: publicado · ✅ win_
  - Formulario en la página; el correo sale por Resend desde Web Promos (dominio verificado) a hello@kinedu.com. Masterclasses reenvía. Honeypot anti-spam.
  - **Resultado:** Probado extremo a extremo, recibido ok. Ahora se registra qué preguntan.
- 🔧 **2026-10-07-01** · Infra · Fix: Clarity ya no cachea el resultado vacío de un 429  _(Implementador)_
  - _estado: publicado · commit ce628d5c4 · ✅ win_
  - El recolector guardaba el 429 como caché del día y lo servía a todas las rutinas. Ahora solo cachea si las 3 llamadas traen datos.
  - **Resultado:** Clarity vuelve a bajar datos completos desde el 8-oct (archivos de 1.8-2.2 MB).
- 🔧 **2026-10-07-02** · SEO · Rec 1: títulos y metas del blog normalizados (3,462 páginas)  _(Implementador)_
  - _estado: publicado · commit f00d8128e · medir: 2026-11-03 · ⏳ por medir_
  - Sufijo ' | Kinedu' uniforme, 0 guiones largos, 60 descripciones reescritas, 10 posts con copy nuevo. Generador scripts/seo/retitle_blog.py idempotente.
  - **Resultado:** Títulos >60 car de 47% a 33%, mediana 59→54.
- 🔧 **2026-10-07-03** · Gift · Rec 2A: /gift pasa utm al checkout de Web Promos  _(Implementador)_
  - _estado: publicado · commit 4db1dcc88 · medir: 2026-10-14 · ⏳ por medir_
  - utm_source=gift-landing solo si la visita no trae utm propio (no pisa campañas). Clic al botón = tag giftcta=checkout en Clarity.
- 🔧 **2026-10-07-04** · Landing · Rec 3: menos fuentes y JS en home y blog  _(Implementador)_
  - _estado: publicado · commit f00d8128e · medir: 2026-11-03 · ➖ neutral_
  - Home sin Google Fonts (Proxima self-hosted pinta todo); translations.js 121KB partido por idioma (-23KB/post comprimido).
  - **Resultado:** Lighthouse móvil neutro dentro del ruido (±9 pts). Ahorro real: -23KB JS/post, -5 fuentes, -2 preconnect. CWV reales en GSC el 3-nov.
- 🔧 **2026-10-08-01** · Contenido · Pieza 1: reescritura primavera PT publicada  _(Implementador)_
  - _estado: publicado · commit f50d58e0e · medir: 2026-11-09 · ⏳ por medir_
  - pt/blog/atividades-primavera: de 712 a 2,843 palabras, 10 H2, FAQPage. Fecha de publicación conservada, Actualizado a hoy.
- 🔧 **2026-10-08-02** · Contenido · Pieza 3: mollera ES + moleira PT publicadas con 301  _(Implementador)_
  - _estado: publicado · commit f50d58e0e · medir: 2026-11-09 · ⏳ por medir_
  - 2 reescrituras (FAQ a 10/11) + 3 redirects 301 permanentes en vercel.json consolidando páginas del mismo tema.

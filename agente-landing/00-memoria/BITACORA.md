# Bitácora de Marina

Registro único de lo que hace el agente de la landing. Generado desde `bitacora.jsonl` (no editar a mano; usar `scripts/agent/bitacora.py`).

Última actualización: 2026-10-12 18:17.


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
  - _estado: pendiente · ⏳ por medir_
  - IAM full-screen EN/ES/PT con brand book, botón al web /gift con utm (inapp/iam/gift-premium) para trackear llegadas y ventas en /analytics. Escala a la caja de CleverTap.
  - **Resultado:** Entregado en ~/Downloads/gift-iam-clevertap. Falta montarlo en CleverTap y apuntar a segmento premium.
- 🔧 **2026-10-12-05** · Proceso · Bitácora de Marina creada  _(Claude)_
  - _estado: publicado · medir: 2026-10-19 · ✅ win_
  - Fuente única bitacora.jsonl + script bitacora.py (add/set/aprende/report) + tablero HTML en ~/Downloads/Marina-Avance. Enganchada a los roles: Implementador anota cada cambio, Medidor lo cierra con resultado+impacto y pega el avance en Slack los lunes.
  - **Resultado:** Sistema funcionando; 12 entradas y 7 aprendizajes sembrados del historial.

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

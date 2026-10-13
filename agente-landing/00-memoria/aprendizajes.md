# Aprendizajes de Marina

Reglas cortas que Marina debe leer ANTES de actuar. Se suben desde la bitácora cuando una medición deja una lección. No repetir lo que ya está aquí.

- **[SEO]** Validar la consulta en Search Console antes de escribir un artículo: un pico x2,900 en impresiones sin que se mueva la posición = tráfico que NO es de papás (caso "oral phase", estudiantes). _(anotado 2026-10-08)_
- **[SEO]** Al reescribir un post NUNCA cambiar la fecha de publicación (Google penaliza); solo actualizar "Actualizado" y dateModified. _(anotado 2026-10-08)_
- **[Infra]** Clarity (y cualquier API con cuota): no cachear el resultado del día si alguna llamada falló; solo cachear cuando TODAS traen datos. _(anotado 2026-10-07)_
- **[Proceso]** `slack_bot.py find` puede devolver el hilo de la semana anterior; cruzar siempre con `read` antes de actuar sobre un "va". _(anotado 2026-10-09)_
- **[A/B]** El beacon del home solo escucha enlaces a app.kinedu.com; hero y badges van a webpromo, así que hay que mandar la variante explícita o el test no se puede leer. _(anotado 2026-10-12)_
- **[Gift]** En IAM y correos de Gift el botón va al web /gift con utm (no deep link kinedu://), porque Gift se compra en web y así se trackea en /analytics → tab Gift. _(anotado 2026-10-12)_
- **[Contenido]** Al consolidar posts con 301, auto-mode bloquea borrar los .html fuente; quedan inalcanzables por el redirect pero hay que borrarlos del repo cuando haya permiso. _(anotado 2026-10-08)_

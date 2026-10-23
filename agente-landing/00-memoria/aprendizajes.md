# Aprendizajes de Marina

- **[SEO]** Correo de Search Console "Página con redirección" (páginas de sitemap sin indexar) = casi siempre efecto esperado de NUESTROS 301 de consolidación, NO un problema. Verificar antes de alarmar: (1) el sitemap solo trae URLs destino; (2) muestra de ~40 URLs del sitemap, todas 200 (alguna 301 = fuga, sacarla del sitemap); (3) cruzar las marcadas con `vercel.json`. Si cuadra: Google indexa el destino, es correcto; reportar como ruido bueno y aclarar que NO es parte de la caída (esa es algorítmica). Mismo criterio para avisos de "404" (cruzar con tráfico antes de 301) y "Rastreada/Alternativa canónica" (contenido delgado → consolidación). _(anotado 2026-10-22)_
Reglas cortas que Marina debe leer ANTES de actuar. Se suben desde la bitácora cuando una medición deja una lección. No repetir lo que ya está aquí.

- **[SEO]**  _(anotado 2026-10-22)_
Reglas cortas que Marina debe leer ANTES de actuar. Se suben desde la bitácora cuando una medición deja una lección. No repetir lo que ya está aquí.

- **[A/B]** Prueba de lectura obligatoria antes de publicar un A/B: mandar un ab_view y un clic de prueba y confirmar que la prueba aparece en abSummary de /api/stats (hero salio ciego 9 dias y el menu desde el 16-oct no se lee). _(anotado 2026-10-20)_
Reglas cortas que Marina debe leer ANTES de actuar. Se suben desde la bitácora cuando una medición deja una lección. No repetir lo que ya está aquí.

- **[Gift]** Para el checkout de Gift medir y bajar fricción en webpromo (es donde muere la intención de compra); la audiencia del in-app no debe ser 'todos premium' sino con intención de regalar (visitó /gift, baby shower) _(anotado 2026-10-15)_
Reglas cortas que Marina debe leer ANTES de actuar. Se suben desde la bitácora cuando una medición deja una lección. No repetir lo que ya está aquí.

- **[SEO]** Validar la consulta en Search Console antes de escribir un artículo: un pico x2,900 en impresiones sin que se mueva la posición = tráfico que NO es de papás (caso "oral phase", estudiantes). _(anotado 2026-10-08)_
- **[SEO]** Al reescribir un post NUNCA cambiar la fecha de publicación (Google penaliza); solo actualizar "Actualizado" y dateModified. _(anotado 2026-10-08)_
- **[Infra]** Clarity (y cualquier API con cuota): no cachear el resultado del día si alguna llamada falló; solo cachear cuando TODAS traen datos. _(anotado 2026-10-07)_
- **[Proceso]** `slack_bot.py find` puede devolver el hilo de la semana anterior; cruzar siempre con `read` antes de actuar sobre un "va". _(anotado 2026-10-09)_
- **[A/B]** El beacon del home solo escucha enlaces a app.kinedu.com; hero y badges van a webpromo, así que hay que mandar la variante explícita o el test no se puede leer. _(anotado 2026-10-12)_
- **[Gift]** En IAM y correos de Gift el botón va al web /gift con utm (no deep link kinedu://), porque Gift se compra en web y así se trackea en /analytics → tab Gift. _(anotado 2026-10-12)_
- **[Contenido]** Al consolidar posts con 301, auto-mode bloquea borrar los .html fuente; quedan inalcanzables por el redirect pero hay que borrarlos del repo cuando haya permiso. _(anotado 2026-10-08)_

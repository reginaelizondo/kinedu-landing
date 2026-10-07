# Backlog de mejoras (vivo)

Formato: [estado] nombre · dato que lo justifica · tipo (A/B o directo) · origen

- [en prueba] Hero móvil B (título corto, botón arriba del fold) · 56% se iba en el hero · A/B desde 6-oct-2026 · reporte Clarity 5-oct · al 6-oct: 15 vistas en A, 8 en B, faltan ~990 por variante
- [en prueba] CTAs en el blog (bloque contextual + barra fija móvil) · blog 48% del tráfico, 1.2% clic saliente · A/B desde 6-oct-2026 · reporte Clarity 5-oct · al 6-oct: 23 vistas en A, 35 en B, faltan ~970 por variante
- [preview] PT primavera reescrita · 2a pagina del sitio, 60,329 impresiones y CTR 0.81% contra 2.79% de la hermana · directo tras vobo · Investigador 6-oct · preview en /pt/blog/preview-atividades-primavera-educacao-infantil, falta vobo para reemplazar la viva
- [preview] Mollera y fontanela consolidadas (ES y PT) · 53,421 impresiones con CTR 0.16%, el peor del sitio con ese volumen · directo tras vobo · Investigador 6-oct · previews en /es/blog/preview-mollera-sumida y /pt/blog/preview-moleira-funda; los 3 301 estan escritos en decisiones.md y NO aplicados
- [pregunta] EN "oral phase" reescritura · la validacion en Search Console tumba la premisa: 56 a 163,483 impresiones en una semana sin moverse de posicion, desktop por encima de movil, consultas de definicion y no de papas; el racimo real son 70 impresiones · Investigador 6-oct · esperando decision de Regina en el hilo
- [pendiente] Quitar los 3 guiones largos de la plantilla del blog (slim CTA, app CTA y tagline del footer) · regla dura de copy, hoy estan en los 3,424 posts · directo · Implementador 6-oct · no se toco en los previews porque es un cambio de plantilla de todo el sitio
- [hecho 7-oct] Títulos y descripciones del blog sin guion largo y con sufijo " | Kinedu" (3,462 páginas) + título y descripción nuevos en los 10 posts de más impresiones y peor CTR · CTR del sitio 0.63% vs 0.68%, 47% de títulos cortados · directo · Estratega 6-oct · medir CTR por página en Search Console el 3-nov (scripts/seo/retitle_blog.py)
- [pendiente] Menú móvil simple (3 ítems arriba) + barra CTA fija al hacer scroll · 267 abren el menú, 124 lo cierran sin elegir · A/B
- [pendiente] Clics muertos del hero (título, imagen) y de las ilustraciones de features a clics útiles · 180 clics muertos/mes · directo
- [en medición] LCP del home de 3.2 s a < 2.5 s · performance 82/100, 66% móvil · directo · 7-oct: home sin Google Fonts y blog con 1 fuente en vez de 6 + translations.js partido por idioma (121 KB a ~40 KB en 3,462 posts); comparar Lighthouse y Core Web Vitals el 3-nov; Lighthouse neutro (home 65 a 68, dentro del ruido): las fuentes de Google nunca se descargaban, el LCP del home está en otra parte (render y hero), eso es lo que hay que buscar; candidato menor: quitar del todo el link de Google Fonts del blog
- [pendiente] Errores JS del índice del blog (anclas con caracteres raros, call stack) · 0.32% de sesiones · directo
- [hecho 6-oct] Contact us: formulario en la página (EN/ES/PT, todo el sitio vía script.js) → /masterclasses/api/contact → webpromo /api/contact → Resend → hello@kinedu.com, reply_to = la persona; fallback a mailto si falla. Probado en vivo. Medición: CTAs "Contact us — opened / sent / fallback mailto / direct mailto" en /analytics. Siguiente: comparar mensajes recibidos en el help desk antes vs después.
- [pendiente] Link app → kinedu.com: 319 sesiones de 1 a 8 s sin clics · revisar con Tech
- [decidido 6-oct] Badges de App Store / Google Play: se quedan en el hero, se miden por clic. Opcional a futuro: apuntarlos al smart.link (Kochava) con creative_id por ubicación para atribuir instalaciones
- [hecho 6-oct] Clarity en Masterclasses (layout, mismo proyecto)
- [pendiente] Masterclasses: embudo tienda → clase → checkout → compra con Clarity, línea base semana 1
- [en medición] Gift: visita → clic → checkout → compra · 13 clics al botón y 1 checkout iniciado en 14 días · directo · 7-oct: enlace al checkout con utm_source=gift-landing y etiqueta giftcta en Clarity; leer en 7 días clics vs llegadas en Web Promos vs checkout_started
- [pregunta] Gift: que el endpoint de Gift registre la llegada a la página de checkout · toca Web Promos (de ahí solo se lee) · preguntado a Regina en el hilo el 7-oct
- [pendiente] Gift parte B: A/B del bloque "qué pasa después" bajo el botón (?gift=a|b, copy exacto en 02-estratega/semana-2026-10-06.md) · después de los 7 días de medición; con 341 vistas/semana tarda ~6 semanas en juntar 1,000 por variante
- [pendiente] Segmento "landing real" en Clarity (sin /privacy, /terms, app.kinedu.com)
- [pendiente] weekly_pull.py: no repetir las llamadas de Clarity si ya hay datos del día en history/ · el 6-oct dieron 429 por gastar el cupo de 10 con dos corridas · directo · Medidor 6-oct
- [pendiente] Search Console, informe de indexación (7-oct): 56 URLs con 404 (error), 9 bloqueadas 403, 88 "rastreada sin indexar", 5 "indexada aunque robots la bloqueaba", 22 noindex (incluye previews). Revisar cuáles de las 404 tienen enlaces o tráfico y poner 301; ver qué bloquea 403. · tarea para el Investigador · origen: correo de GSC 7-oct

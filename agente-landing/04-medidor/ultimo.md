# Medición · lunes 12 de octubre de 2026

Fuente: `weekly-2026-10-12.json` contra `weekly-2026-10-06.json`, más una consulta extra a Search Console por semana (3 al 9 de octubre contra 26 de septiembre al 2 de octubre). Clarity sí entregó datos esta vez (3 días, 3,565 sesiones, 1,022 de bots).

## Alerta mayor: Google nos manda la mitad de clics desde el 3 de octubre
- Semana 3 al 9 de octubre: 1,040 clics. Semana anterior: 2,068. Cae 49.7%. La de antes (19 al 25 de septiembre) fue 2,372. Los días 3 al 6 ya están cerrados y van en 160 a 184 clics diarios contra 350 a 400 la semana previa. No es efecto de datos sin cerrar.
- Blog: 1,644 a 692 clics (cae 58%). Resto del sitio: 442 a 363 (cae 18%). Páginas con al menos un clic: 436 a 303.
- Todos los países caen: Brasil 834 a 320, EE. UU. 203 a 116, México 202 a 147, Portugal 194 a 82. Móvil 1,513 a 762, escritorio 541 a 264 (posición escritorio 8.7 a 21.5).
- Las que más pierden: /pt/blog/atividades-criancas-1-ano 60 a 4, /pt/blog/atividades-primavera 50 a 1, /pt/blog/atividades-maternal 45 a 2, /pt/blog/bebe-dorme-de-boca-aberta 44 a 7, /es/blog/actividades-maternal 35 a 4, /blog/baby-fake-cough 44 a 16. El home aguanta: 244 a 195, posición 3.5 a 3.3.
- La caída empieza el 2 y 3 de octubre, antes del retítulo masivo del 7 de octubre y antes de los A/B del 6. No la causamos nosotros, pero el retítulo cae en medio y va a estorbar su lectura el 3 de noviembre.
- Contexto externo: reportes del sector ubican la segunda fase del "September 2026 Spam Update" de Google el 30 de septiembre y su cierre entre el 4 y 6 de octubre. Coincide en fechas. No lo puedo confirmar desde aquí.
- El dato de 28 días lo esconde: 7,798 clics contra 7,590 (sube 2.7%) porque las primeras tres semanas fueron buenas. Posición 28d 8.7 contra 11.3, CTR 0.61% contra 0.71%.
- Para el Analista: abrir Search Console y revisar acciones manuales y problemas de seguridad, y comparar por consulta la semana 3 al 9 contra la anterior en Brasil. Para el Estratega: congelar cambios masivos de plantilla hasta leer la semana que entra.

## A/B vivos
- Hero móvil: NO SE PUEDE LEER. A 488 vistas (EN 341, ES 91, PT 56), B 363 (EN 232, ES 81, PT 50), 0 clics en las dos. El motivo es un hueco de tracking: el beacon de conversión del home solo escucha enlaces a app.kinedu.com y el botón del hero apunta a webpromo.kinedu.com/p/landing-kinedu. La etiqueta "Hero, Try Free" nunca ha aparecido en /api/stats. Los badges de App Store (85 clics) y Google Play (53) están en el hero pero se mandan sin variante.
- Instrucción para el Implementador (técnico, sin efecto visible, directo): en index.html, es/index.html y pt/index.html, bloque inline cerca de la línea 718: (1) escuchar el clic en `.hero-ctas a` y mandar conversion "Hero, Try Free" con `variant` cuando sea móvil; (2) agregar `variant` a las conversiones de App Store Badge y Google Play Badge en móvil; (3) si localStorage falla (el catch), no mandar `ab_view`. Anotar la fecha del arreglo: las 1,000 vistas por variante se cuentan desde ahí.
- Reparto desbalanceado en el hero: EN 341 contra 232 cuando se esperan 286 y 286 (z 4.6). Causa probable: navegadores sin storage caen en "a" por defecto (Clarity ve 566 sesiones en navegadores de Instagram y Facebook). El punto (3) de arriba lo corrige.
- Blog CTAs: A 883 vistas y 8 clics (0.91%). B 787 vistas y 13 clics (1.65%). B va 82% arriba. Prueba z: 1.37, p 0.17. No es significativo. Faltan 213 vistas en B y un día para los 7 mínimos; con 130 vistas diarias se lee el lunes 19. No se apaga: B no va abajo.
- Blog por idioma: EN A 1 de 321 (0.3%), B 5 de 275 (1.8%). PT A 4 de 298 (1.3%), B 7 de 252 (2.8%). ES A 3 de 264 (1.1%), B 1 de 260 (0.4%). El reparto del blog también se inclina a A (883 contra 787, z 2.4), mismo motivo.
- Confirmación en webpromo: el JSON no trae utm_source=blog. El placement landing-kinedu junta hero y blog: 456 llegadas, 104 correos, 6 pagadas en 14 días. No se puede atribuir por variante. Un clic no es una venta.

## Recomendaciones de la semana pasada
- Estratega 1 (títulos sin guion, sufijo Kinedu): hecho el 7 de octubre. Dato: los clics del blog cayeron 58% la semana siguiente, pero la caída empezó antes del cambio. Lectura limpia el 3 de noviembre, con la alerta de arriba encima.
- Estratega 2A (utm y etiqueta Clarity en /gift): hecho el 7 de octubre. Desde entonces 0 checkouts iniciados en el endpoint de Gift. 13 clics al botón de checkout en 14 días (el JSON no los parte por día). El lado Web Promos sigue en pregunta. 2B (A/B "qué pasa después"): no se hizo, esperaba esta lectura. Ojo: el 8 de octubre el precio de /gift bajó a $49.99 (commit af07d6af9, fuera del agente); cambia la base de medición.
- Estratega 3 (fuentes y translations partido): hecho el 7 de octubre. Lighthouse neutro, 65 a 68 en el home.
- Investigador 6-oct, pieza 1 (primavera PT): publicada el 8 de octubre. 28 días: 375 clics contra 224. Pero la semana 3 al 9 cayó de 50 a 1 clic, posición 7.7 a 8.5. Demasiado pronto y con la caída general encima.
- Investigador 6-oct, pieza 3 (mollera ES y moleira PT): publicada el 8 de octubre con 3 redirects 301. 28 días: mollera-sumida 57 clics (antes 42), moleira-funda 20 (antes 35). Semana: mollera 19 a 1.
- Investigador 6-oct, pieza 2 (oral phase): no se escribió; Regina pidió consolidar. Falta que el Investigador diga qué página queda.
- Investigador 9-oct (3 piezas): previews listos el 12 de octubre, esperan el "va". Nada publicado.
- Sin avance: menú móvil, clics muertos, errores JS del blog, link app a web, segmento Clarity, indexación GSC (56 URLs con 404). Sí avanzó: el recolector ya reutiliza Clarity del día y no cachea errores (7 de octubre).

## Semana vs semana por área (cambios de más de 15% marcados con ALERTA)
- Sitio (api/stats, 6 al 12 de octubre con hoy incompleto, contra 29 de septiembre al 5): visitas 5,504 contra 7,319 (cae 24.8%, ALERTA). Únicos 1,997 contra 2,284 (cae 12.6%). Conversiones 155 contra 216 (cae 28.2%, ALERTA). CVR 7.8% contra 9.5% (cae 17.9%, ALERTA). Referidor google.com en 14 días: 4,183 contra 5,628.
- Google: ver alerta mayor. Semana 1,040 contra 2,068 clics (ALERTA). Posición semanal 11.1 contra 8.5.
- Masterclasses (14 días): visitors 329 contra 314 (sube 4.8%). classViews 256 contra 184 (sube 39%, ALERTA). checkoutsStarted 34 contra 13 (sube 162%, ALERTA). purchases 3 contra 3. revenue en ventana $0 contra $0 (el endpoint reporta $0 con 3 compras, problema conocido). El 7 de octubre hubo 18 checkouts, 13 de First Aid, 0 compras; fuente "email" 178 visitas: huele a campaña.
- Gift (14 días): paid 1 contra 1. Es la misma venta del 30 de septiembre (BRL 299.90). Cero desde entonces.
- Assessment (14 días): completed 95 contra 92 (sube 3%). purchases 54 contra 54 (sin cambio; el número parece acumulado, no de 14 días).
- Webpromo landing-kinedu (14 días): llegaron 456 contra 503 (cae 9.3%). Correos 104 contra 123 (cae 15.4%, ALERTA). Pagadas 6 contra 9 (cae 33%, ALERTA). Ingreso $463 contra $683.
- Raro, para el Analista: /pt/blog (índice) pasa de 493 a 859 vistas y app.kinedu.com como referidor de 159 a 251. Puede ser un enlace nuevo desde la app.

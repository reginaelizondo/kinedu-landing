# Medición · lunes 9 de noviembre de 2026

Fuente: `weekly-2026-11-09.json` contra `weekly-2026-11-02.json`. Sin errores en el pull. Clarity no se revisó aquí. Ojo: abSummary es una ventana de 14 días.

## A/B vivos (CVR = clics al CTA entre vistas)
- **herobtn (azul A, naranja B), abierto 27-oct, 13 días:** total A 114/845 (13.5%), B 136/961 (14.2%), lift +5%, z 0.41, p 0.69. EN A 74/534 (13.9%), B 95/671 (14.2%). ES 16.4% vs 17.8%. PT 7.8% vs 8.6%.
- **herocopy ("today" A, "every single day" B):** total A 126/899 (14.0%), B 124/907 (13.7%), lift -2%, p 0.83. EN 13.3% vs 14.7%. ES A 20.8% vs B 13.1% (-37%, p 0.055, 175 vistas). PT 7.3% vs 9.1%.
- **Lección:** el 2-nov EN decía naranja +51% (17.5% vs 11.6%, n=485). Con n=1,205 es +2%. Era ruido temprano.
- **Sin ganadora:** la variante más chica es 845 (herobtn) y 899 (herocopy), menos de 1,000. Faltan **155 vistas en herobtn A** y **101 en herocopy A** en total; por idioma EN faltan ~470 en herobtn A, ES y PT no llegan en semanas. Hay más de 7 días, pero no hay muestra. No hay motivo para apagar: ninguna B va más de 10% abajo con 500+ vistas (ES copy B -37% tiene 175 vistas).
- **Instrucción al Implementador:** ninguna hoy. Con ~100 vistas diarias en total, el corte de 1,000 por variante cae el 11-12 nov. Leer el jueves 12 y decidir con 95%. Si sigue plano, fijar lo que prefiera Regina (azul o naranja da lo mismo en CVR).
- **menú móvil:** total A 19/82 (23.2%), B 35/113 (31.0%), +34%, p 0.23. Muestra mínima (ventana rodante), faltan ~900 vistas en A. B va arriba. Sigue.
- **hero (layout) y blog:** cerrados (B fijo). Restos en el JSON: hero 99 y 100 vistas, blog 1 y 2.
- **Confirmación webpromo landing-kinedu (7 d):** llegaron 522 (529), correos 98 (108, -9%), iniciaron 33 (30), pagadas 6 (5), ingreso $440 ($392). Junta hero y blog, no se parte por variante ni trae utm_source=blog. Un clic no es una venta.

## Recomendaciones de la semana pasada
- Estratega 1 (barra fija en clases de Masterclasses): **no se hizo**. Necesita "dale" y vive en otro repo. Dato ahora: vistas de clase 28 en 14 d (antes 557), checkouts 3 (1). El push de 29-oct y 1-nov salió de la ventana; el problema se queda sin medir.
- Estratega 2 (`?lang=es|pt` en el Try free de ES y PT): **no se hizo**. `es/index.html` sigue sin `lang=`. Sí salió el 4-nov el home ES/PT traducido en HTML crudo y links de nav corregidos (GEO, otra tarea). Propuesta repetida desde el 12-oct.
- Estratega 3 (reescribir ES maternal y PT 1 ano): **no se hizo**. Sin commits en esas páginas.
- Investigador 5-nov (animales PT, tamaño del bebé PT, leche materna EN): **no se hizo**. Sin commits; no pude abrir el hilo del Estratega para ver si hubo "dale". Siguen en preview (sin "va"): PT garrafa PET y ES nodriza.
- Google en esas páginas: no se puede leer, no se tocaron.

## Semana vs semana (cambios de más de 15% marcados con ALERTA)
- **Sitio** (JSON, 7 d contra 7 d previos): visitas 6,015 (5,636, +6.7%), únicos 2,011 (1,965), conversiones 277 (276), CVR 13.8% (14.0%). Estable. Contra el reporte del 2-nov: visitas +12%, conversiones +8%.
- **Google** (28 d, 10-oct al 6-nov contra 12-sep al 9-oct): clics 5,508 contra 7,798 (**-29%, ALERTA**), impresiones 885,960 contra 1,278,098 (-31%), posición 9.9 contra 8.7. Blog 3,816 contra 5,757; resto 1,452 contra 1,723. La semana 31-oct al 6-nov: 1,638 clics contra 1,691 (-3%). Diario estable en 184 a 281. Se estabilizó sin recuperarse.
- **Bing** (28 d): clics 476 (536, -11%).
- **Masterclasses** (14 d): visitors 326 contra 582 (**-44%, ALERTA**), storefront 349 contra 109 (**+220%, ALERTA**), classViews 28 contra 557 (**-95%, ALERTA**), checkouts 3 contra 1, purchases 0 contra 0, revenue $0. Cayó la oleada de push; hoy casi todo entra por la portada.
- **Gift** (14 d): checkout_viewed 8 (2), checkout_started 2 (0), created 2, paid 0. Los 2 vienen de gift-landing en EN el 6-nov. Sitio: "Gift, See plans" 17 clics (22), 89 vistas de /gift (99).
- **Assessment**: started 123 (120), completed 106 (104, +2%), cuentas 160 (148), purchases 54 (sin cambio, acumulado). Webpromo assessment-landing: llegaron 44 (35, +26%), correos 2 (0), iniciaron 1, pagadas 0.
- **Webpromo landing-kinedu**: ver arriba. Cambios dentro de 15%.

## Para el Analista y el Estratega
- El hero no mueve CVR (14% en las dos pruebas). Dejar de gastar semanas en el hero y mirar lo que viene después del clic: de 522 llegadas hay 98 correos (19%) y 6 pagadas.
- Guardia avisó el 9-nov: conversiones de ayer 23, -47% contra el promedio de 43. Dato de un domingo; no cambia la semana.
- Tres recomendaciones del Estratega llevan sin "dale" ni ejecución. Preguntar en el hilo cuál se descarta.

# Medición · lunes 16 de noviembre de 2026

Ojo con la fuente: el pull de hoy no terminó (weekly_pull.py cortado por tiempo). Uso `weekly-2026-11-12.json` (generado el 12-nov 11:00, sin errores). Los datos llegan hasta el 9 al 12-nov. El JSON del 9-nov ya no está en disco: comparo contra los números del reporte del 9-nov. abSummary es una ventana de 14 días.

## A/B vivos (CVR = clics al CTA entre vistas)
- **herobtn (azul A, naranja B), abierto 27-oct, 20 días:** A 144/1,045 (13.8%), B 149/1,121 (13.3%), lift **-4%**, z -0.33, p **0.74**. EN 14.5% vs 13.9%. ES 14.5% vs 14.9%. PT 9.8% vs 7.3% (-26%, 153 y 137 vistas).
- **herocopy ("today" A, "every single day" B):** A 142/1,099 (12.9%), B 151/1,065 (14.2%), lift **+10%**, z 0.85, p **0.39**. EN 11.9% vs 16.5% (+38%). ES 18.1% vs 10.8% (-40%). PT 9.5% vs 7.8%.
- **Veredicto: sin ganadora.** La variante más chica ya tiene más de 1,000 y pasaron más de 7 días, pero p es 0.74 y 0.39. No hay ninguna B más de 10% abajo con 500+ vistas en total. El +51% del naranja (2-nov) y el +38% de EN en copy son ruido por idioma.
- **Instrucción al Implementador:** ninguna ganadora que fijar. Cierre propuesto por el Estratega (9-nov): "fijar B en el hero móvil: quitar el reparto y dejar hero--b (botón naranja) y dejar el copy A (today); apagar herobtn y herocopy". Solo con "dale" de Regina, Paola o Pepis (el hero lo necesita). Sin "dale", los dos siguen corriendo.
- **menú móvil:** A 16/90 (17.8%), B 30/102 (29.4%), **+65%**, z 1.88, p **0.059**. Casi 95%, pero 90 y 102 vistas, faltan ~900 en A. B va arriba, sigue.
- **hero (layout) y blog:** cerrados con B fijo (restos: hero 14 vistas, blog 0).
- **Confirmación webpromo landing-kinedu (7 d):** llegaron 507 (522), correos 94 (98, -4%), iniciaron 27 (33), pagadas 5 (6), ingreso $395 ($440, -10%). Junta hero y blog, no se parte por variante ni trae utm_source=blog. Los clics del hero no se ven como más ventas. Un clic no es una venta.

## Recomendaciones de la semana pasada
- Estratega 1 (cerrar hero el 12-nov y definición "Kinedu es..."): **no se hizo**. El A/B sigue vivo sin decisión; la definición no salió. Dato: sin ganadora, cerrar es de gusto.
- Estratega 2 (`?lang=es|pt` en el Try free de ES y PT): **no se hizo**. Propuesta repetida desde el 12-oct. PT sigue con el CVR más bajo del hero (7 a 10%).
- Estratega 3 (reescribir PT "atividades criancas 1 ano"): **no se hizo**. Sin commits en esa página.
- Investigador 12-nov (calculadora ES, mãos fechadas PT, tamanho do bebê PT): **hecho como PREVIEW** el 13-nov (8161421a, noindex, sin enlazar), revisado en celular por Paola. **No publicado**: falta "va". Sin datos de Google aún.
- Otros cambios del sitio (no eran recomendaciones): 12-nov Leadpages paso 1 (27 links de la landing a webpromo y masterclasses), 11-nov correos de Gift de temporada.

## Semana vs semana (cambios de más de 15% marcados)
- **Sitio** (JSON 12-nov, 7 d contra 7 d previos): visitas 9,319 contra 5,099 (**+83%, ALERTA, ver nota**), únicos 2,086 contra 1,955, conversiones 306 contra 278 (+10%), CVR 14.7% contra 14.2%. Las visitas suben y los únicos no: huele a páginas por visita o tráfico no humano; las conversiones y el CVR están estables. Nota: contra el 9-nov (6,015 visitas) también es +55%. Pedir al Analista revisar.
- **Google** (28 d, 13-oct al 9-nov contra 15-sep al 12-oct): clics 5,820 contra 7,245 (**-20%, ALERTA**), impresiones 959,049 contra 1,199,298 (-20%), CTR 0.61% (igual), posición 9.8 contra 8.7. Última semana (3 al 9-nov) 1,634 clics contra 1,627 (0%). Plano, sin recuperar.
- **Bing** (28 d): clics 496 contra 521 (-5%).
- **Masterclasses** (14 d): visitors 394 (326, +21%), storefront 359 (349), classViews 89 (28, **+218%, ALERTA**), checkoutsStarted 15 (3, **ALERTA**), purchases 0 (0), revenue $0. Hubo otra oleada el 7-nov (199 vistas). 15 checkouts y 0 compras: el cuello es el checkout.
- **Gift** (14 d): checkout_viewed 14 (8), checkout_started 3 (2), created 3, **paid 0**.
- **Assessment**: started 124 (123), completed 106 (106), cuentas 162 (160), purchases 54 (54). Webpromo assessment-landing: llegaron 50 (44), correos 2, pagadas 0.

## Para el Analista y el Estratega
- Dos pruebas de hero, 2,200 vistas cada una y cero diferencia. Cerrar y dejar de medir el hero. Lo que falta está después del clic: 507 llegadas, 94 correos, 5 pagadas.
- Masterclasses: 15 checkouts sin ninguna compra en 14 días. Revisar el checkout.
- Tres recomendaciones del Estratega llevan 2 semanas sin "dale". Preguntar en el hilo cuáles se descartan.
- Pull de hoy: revisar por qué weekly_pull.py pasa de 25 min (antes 3 a 5).

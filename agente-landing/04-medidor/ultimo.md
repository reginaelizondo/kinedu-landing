# Medición · lunes 23 de noviembre de 2026

Fuente: `weekly-2026-11-23.json` (generado hoy, sin errores) contra `weekly-2026-11-17.json`. abSummary y Masterclasses/Gift son ventanas de 14 días; el sitio es 7 d contra 7 d previos; Google 28 d (24-oct al 20-nov).

## A/B (CVR = clics al CTA entre vistas, 14 d)
- **herobtn (azul A, naranja B): CERRADO el 18-nov** (naranja fijo). Final: A 10.5% (102/968), B 9.2% (87/947), lift -13%, p 0.32. Con el corte del 16-nov: 13.8% vs 13.3%, p 0.74. Sin ganadora, nunca hubo diferencia. B no pasa el umbral de apagar (-13% pero p 0.32).
- **herocopy ("today" A, "every single day" B): CERRADO el 18-nov** ("today" fijo). Final: A 9.0% (88/973), B 10.8% (101/938), +19%, p 0.21. Sin ganadora. EN B 12.0% vs 9.1%, ES y PT iguales: ruido.
- Los dos arrastran vistas del 9 al 17-nov dentro de la ventana de 14 d; no sigue habiendo reparto. Instrucción al Implementador: ninguna. Revisar en 7 días que el reparto ya no mande beacons.
- **Menú móvil (único A/B vivo):** A 22.0% (27/123), B 32.3% (43/133), **+47%**, z 1.86, **p 0.06**. EN 20.2% vs 33.0% (89 y 97 vistas), ES 26.3% vs 23.5%, PT 26.7% vs 36.8%. Sin 95%. **Faltan ~880 vistas en A** (y ~870 en B) para 1,000; al ritmo de 123 por 14 d tarda más de 3 meses. B no va abajo: no se apaga. Instrucción: ninguna; decidir si se fija B por gusto, porque la muestra no llegará pronto.
- **hero (layout) y blog:** cerrados (hero 1 vista, blog 0).
- **Webpromo landing-kinedu (7 d):** llegaron 560 (532, +5%), correos 119 (114), iniciaron 25 (26), pagadas 5 (6), ingreso $389.24 ($485.52, **-20%**). El JSON no trae utm_source=blog ni parte por variante. Un clic no es una venta: el clic del hero no cambió con color ni copy y las ventas siguen en 5 a 6 por semana.

## Recomendaciones de la semana pasada
- Estratega 17-nov 1 (Masterclasses: confirmar acceso en el pago y botón "Empezar mi clase"): **no se hizo**. Paola dijo "espera" el 20-nov (lo hacen ellas en la app). Dato: checkouts 20 (13), compras 1 (1), de 6 compradores 0 han empezado una clase. Sigue abierto.
- Estratega 17-nov 2 (fuente en la calculadora ES): **se hizo** el 18-nov (ACOG, b9a378ac). Calculadora ES publicada el 17-nov; su efecto en Google se mide desde el 15-dic (28 d).
- Estratega 17-nov 3 (cerrar hero y definición "Kinedu es..."): **se hizo** el 18-nov (hero fijo naranja + today, definición EN/ES/PT). Efecto: CVR del sitio 13.7% (13.8%), plano, como se esperaba.
- Investigador 19-nov: título ES cuidados del recién nacido, metas y sección "hambre en el vientre" EN/PT **hechos** el 21-nov (directo). Nodriza ES y cobertor PT quedaron como PREVIEW noindex: **falta "va" de Paola**. Sin datos de Google aún (muy reciente).
- Pendientes sin respuesta: `?lang=es|pt` (6 semanas) y reescritura PT "atividades criancas 1 ano" (3 semanas).

## Semana vs semana (marcado si pasa de 15%)
- **Sitio 7 d:** visitas 9,373 (15,886, **-41%**; la semana previa traía el pico de www.aocr.org), únicos 2,183 (2,349, -7%), conversiones 299 (323, -7%), CVR 13.7% (13.8%). Referido www.aocr.org ahora 252 (antes 1,068): el tráfico raro bajó.
- **Google 28 d:** clics 6,999 (5,287, **+32%**), impresiones 1,196,385 (949,587, **+26%**), CTR 0.59%, posición 9.3 (9.5). Contra el corte de la semana pasada (6,610) sube 6%. Recuperación real. Bing 564 clics (496, **+14%**, casi).
- **Masterclasses 14 d:** visitors 428 (484, -12%), classViews 297 (211, **+41%**), checkoutsStarted 20 (13, **+54%**), purchases 1 (1), revenue $34.99 (igual). Fuentes: directo 336, email 116, push 58. Cuello: 20 checkouts, 1 compra (5%).
- **Gift 14 d:** checkout_viewed 13 (14), started 3 (5, **-40%**, base chica), paid 2 (2), ingreso $119.98. Los correos de Gift con utm_source=email se miden en la tabla Campañas (utm) de /analytics; el JSON no las trae.
- **Assessment:** started 132 (130), completed 111 (110), cuentas 189 (179, +6%), purchases 55 (55). Webpromo assessment-landing: llegaron 37 (52, **-29%**), correos 1, pagadas 0.

## Para el Analista y el Estratega
- El hero ya no es palanca: 4,000 vistas entre dos pruebas, cero efecto. Lo que falta está después del clic (560 llegan, 119 correos, 5 pagan).
- Masterclasses: la demanda sube (+41% clases vistas, +54% checkouts) y la compra no. Ya está en manos de Paola/app.
- Google se recupera: hacer seguimiento de las URLs publicadas el 17-nov y 21-nov antes de tocar más plantilla.
- Menú móvil: decidir fijar B sin 95% o dejarlo corriendo meses.

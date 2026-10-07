# Medición · lunes 6 de octubre de 2026

Primer ciclo. No existe `02-estratega/semana-*.md`, así que el cierre va contra el backlog y el reporte Clarity del 5 de octubre.

## A/B vivos (sin muestra)
Los dos A/B se encendieron hoy, así que solo hay horas de datos.

- Hero móvil: A 15 vistas y 0 clics. B 8 vistas y 0 clics. Faltan 985 vistas en A y 992 en B.
- Blog CTAs: A 23 vistas y 0 clics. B 35 vistas y 2 clics (los dos en inglés). Faltan 977 en A y 965 en B.
- Sin ganadora. Ninguna instrucción para el Implementador esta semana.
- Ojo el próximo lunes: el hero en portugués va 4 vistas en A y 0 en B. Con esa n no significa nada, pero si B sigue en 0 hay que revisar el reparto en /pt.

## Semana vs semana (api/stats, 30 sep al 6 oct vs 23 al 29 sep)
- Visitas: 6,183 vs 7,356. Baja 15.9%. Alerta. El tramo de hoy va incompleto.
- Visitantes únicos: 1,944 vs 2,338. Baja 16.9%. Alerta.
- Conversiones: 197 vs 164. Sube 20.1%. Alerta.
- CVR: 10.1% vs 7.0%. Sube 44.5% relativo. Alerta.
- Menos tráfico y más conversión. El Analista debe confirmar si viene de Gift (79 clics a "Gift, ver planes" y 13 a checkout en 14 días) o de un día suelto.

## SEO (Search Console, 6 sep al 3 oct vs 9 ago al 5 sep)
- Clics: 8,775 vs 7,262. Sube 20.8%. Alerta.
- Impresiones: 1,393,786 vs 1,075,750. Sube 29.6%. Alerta.
- Posición media: 8.8 vs 11.4. Mejora 2.6 posiciones.
- CTR: 0.63% vs 0.68%. Baja 6.7%. Efecto normal de ganar impresiones.
- Blog: 6,553 vs 5,254 clics, sube 24.7%. Resto del sitio: 1,883 vs 1,755, sube 7.3%.
- Sube /pt/blog/atividades-primavera-educacao-infantil, de 113 a 490 clics (estacional de Brasil). /founder entra con 32 clics desde cero.
- Baja la home /pt, 49 clics menos. Nada más baja más de 21 clics. Los últimos días del rango no están cerrados, por eso el 3 de octubre se ve bajo.

## Recomendaciones de la semana pasada
- Hero móvil B: hecho. A/B encendido hoy (97cc5878b).
- CTAs del blog: hecho. A/B encendido hoy (a6cd93600).
- Clarity en webpromo: hecho el 5 de octubre. Clarity en Masterclasses: hecho hoy.
- Contact us: Regina decidió hoy el formulario corto a hello@kinedu.com, como A/B contra el mailto. Sin implementar.
- Menú móvil, clics muertos del hero, LCP del home, errores JS del blog, link app a web, segmento "landing real", líneas base de Masterclasses y Gift: sin avance.

## Falla de datos
Clarity devolvió 429 en sus tres llamadas (totales, por URL, por dispositivo). El recolector ya había corrido hoy y se gastó el cupo diario. Esta semana no hay Clarity en el JSON. Hay que evitar la doble corrida del mismo día.

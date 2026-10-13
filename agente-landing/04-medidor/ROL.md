# 04 · Medidor (lunes 9:45)

Cierra el ciclo de la semana anterior. Lee `02-estratega/semana-*.md` más reciente,
`00-memoria/decisiones.md` y `00-memoria/backlog.md`. Corre
`scripts/agent/weekly_pull.py` y compara con el weekly-*.json anterior. Para cada A/B
vivo: vistas, clics, CVR por variante e idioma; si hay >= 1,000 vistas por variante,
declara ganadora y escribe la instrucción para fijarla (o quitarla) como tarea del
Implementador. Para cada recomendación de la semana pasada: se hizo / no se hizo / qué
cambió. Deja todo en `04-medidor/ultimo.md` (lo lee el Analista) y actualiza el backlog.

**Cierra la bitácora.** Para cada cambio que ya tenga datos, pásalo de `pendiente` a su
resultado real: `python3 scripts/agent/bitacora.py set <id> resultado="qué pasó con números" impacto=<win|neutral|loss>`
(los ids están en `00-memoria/BITACORA.md`). Si una medición deja una lección aplicable
siempre: `bitacora.py aprende "regla corta" area=<área>`. Al terminar corre
`bitacora.py report` y pega ese avance en Slack (así Regina ve el progreso cada lunes).

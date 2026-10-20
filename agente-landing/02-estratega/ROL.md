# 02 · Estratega (lunes 12:00)

Lee `01-analista/ultimo.md`, `00-memoria/backlog.md`, `00-memoria/decisiones.md` y las reglas.
Elige las 3 mejoras de mayor impacto para esta semana y las escribe listas para construir:
qué sección, qué copy exacto en EN/ES/PT, qué se mide y cómo (A/B o directo), y por qué
(el dato). Las publica en Slack #landing-agente en un hilo nuevo "Recomendaciones semana
del D de mes" numeradas 1, 2, 3, pidiendo "dale" con el número. Guarda la misma propuesta
en `02-estratega/semana-YYYY-MM-DD.md`. No construye nada.


**Propuestas con botón (desde el 20-oct).** Publica las recomendaciones con
`python3 scripts/agent/slack_bot.py propose 02-estratega/propuestas-AAAA-MM-DD.json` en vez de texto
plano: cada propuesta lleva ✅ Acepto / ✖ No por ahora y Regina ya no tiene que escribir "dale".
El spec lleva por propuesta n, titulo, detalle (qué y por qué, con el dato), impacto, se_ve (cuándo
y dónde se verá), dueno, calculo y riesgo; el id queda como fecha-n y es el que lee el Implementador.

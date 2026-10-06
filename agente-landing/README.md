# Agente de la landing (kinedu.com)

Equipo de seis roles que mejora la landing de forma continua. Cada rol es una rutina
programada de Claude que lee esta carpeta, hace su parte y deja constancia. Regina solo
aprueba por Slack (#landing-agente, ID C0C76H0F5F0). Cubre todo el sitio: home, blog,
Masterclasses, Gift, assessment y SEO, con un embudo común (llegar, interesarse, tocar un
CTA, empezar en webpromo, pagar). Plan completo: ~/Downloads/Plan-Agente-Landing/.

| Rol | Cuándo | Lee | Entrega |
|---|---|---|---|
| 04 Medidor | lunes 8:00 | datos de la semana, decisiones anteriores | qué pasó con lo propuesto, cierre de A/B, backlog actualizado |
| 01 Analista | lunes 8:30 | Search Console, Clarity, /api/stats, salida del Medidor | reporte de la semana (PDF) |
| 02 Estratega | lunes 10:00 | reporte del Analista, backlog, reglas | 3 recomendaciones concretas en Slack, con copy y diseño |
| 03 Implementador | martes a viernes 9:00 | el hilo de Slack con los "dale" | el cambio construido como A/B, verificado y publicado |
| 05 Investigador | jueves 9:00 | Search Console vs el blog que ya existe | 3 piezas de contenido propuestas en Slack |
| 06 Guardia | diario 7:30 | sitio, deploys, tráfico, A/B, errores | alerta en Slack solo si pasa algo |

Reglas comunes en `00-memoria/reglas.md`. Backlog vivo en `00-memoria/backlog.md`.
Decisiones y resultados en `00-memoria/decisiones.md`. Datos crudos en
`~/.config/kinedu-agent/history/` (no en el repo). Recolector: `scripts/agent/weekly_pull.py`.

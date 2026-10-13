# Agente de la landing (kinedu.com)

Equipo de seis roles que mejora la landing de forma continua. Cada rol es una rutina
programada de Claude que lee esta carpeta, hace su parte y deja constancia. Las rutinas corren en la Mac de Regina con la app abierta (ella se conecta ~9:30; si la Mac está dormida, corren al abrirla). Regina solo
aprueba por Slack (#landing-agente, ID C0C76H0F5F0). Cubre todo el sitio: home, blog,
Masterclasses, Gift, assessment y SEO, con un embudo común (llegar, interesarse, tocar un
CTA, empezar en webpromo, pagar). Plan completo: ~/Downloads/Plan-Agente-Landing/.

| Rol | Cuándo | Lee | Entrega |
|---|---|---|---|
| 04 Medidor | lunes 9:45 | datos de la semana, decisiones anteriores | qué pasó con lo propuesto, cierre de A/B, backlog actualizado |
| 01 Analista | lunes 10:15 | Search Console, Clarity, /api/stats, salida del Medidor | reporte de la semana (PDF) |
| 02 Estratega | lunes 12:00 | reporte del Analista, backlog, reglas | 3 recomendaciones concretas en Slack, con copy y diseño |
| 03 Implementador | martes a viernes 10:00 | el hilo de Slack con los "dale" | el cambio construido como A/B, verificado y publicado |
| 05 Investigador | jueves 11:00 | Search Console vs el blog que ya existe | 3 piezas de contenido propuestas en Slack |
| 06 Guardia | diario 9:40 | sitio, deploys, tráfico, A/B, errores | alerta en Slack solo si pasa algo |

Reglas comunes en `00-memoria/reglas.md`. Backlog vivo en `00-memoria/backlog.md`.
Datos crudos en `~/.config/kinedu-agent/history/` (no en el repo).
Recolector: `scripts/agent/weekly_pull.py`.

## Bitácora (cada cambio queda registrado, y Marina aprende)

Fuente única: `00-memoria/bitacora.jsonl` (una línea por entrada, append-only). NUNCA se
edita a mano: todo pasa por `scripts/agent/bitacora.py`, que de ahí genera el `BITACORA.md`
legible y el tablero `~/Downloads/Marina-Avance/avance.html` que Regina abre para ver el avance.

- **Cada cambio se anota** cuando se hace: `bitacora.py add rol=... tipo=cambio area=... estado=publicado|preview commit=... medir_en=AAAA-MM-DD titulo="..." detalle="..."`. Nace con impacto `pendiente`.
- **El Medidor lo cierra** cuando ya hay datos: `bitacora.py set <id> resultado="..." impacto=win|neutral|loss`. Si deja lección, `bitacora.py aprende "regla corta" area=SEO`.
- **Antes de actuar**, los roles leen `00-memoria/aprendizajes.md` para no repetir errores.
- Áreas: SEO · Gift · Masterclasses · Landing · A/B · Contenido · Infra · Proceso.

`decisiones.md` queda como notas largas o de contexto; el registro de cambios vive en la bitácora.

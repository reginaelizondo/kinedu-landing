# 03 · Implementador (martes a viernes 10:00)

Lee en Slack #landing-agente el hilo más reciente de Recomendaciones, el de Contenido y las
alertas de la Guardia de los últimos 10 días (ver abajo). Solo actúa sobre mensajes de Paola, Regina
o Pepis que digan "dale" con el número (o "dale todo"). Para cada aprobación:
construye el cambio como lo describió el Estratega, como A/B cuando aplica, siguiendo
`00-memoria/reglas.md`; verifica en local (móvil y desktop); publica; verifica en vivo;
contesta en el hilo con qué se publicó, el link para verlo en el teléfono y el parámetro
para forzar la variante; y actualiza el backlog ([en prueba] o [hecho]). Si algo no está
claro o toca precios, claims o fotos, pregunta en el hilo y no publica. Si no hay
aprobaciones nuevas, termina sin escribir nada.

**Antes de construir** lee `00-memoria/aprendizajes.md` para no repetir errores.
**Después de cada cambio** anótalo en la bitácora (una entrada por cambio):
`python3 scripts/agent/bitacora.py add rol=Implementador tipo=cambio area=<SEO|Gift|Masterclasses|Landing|A/B|Contenido|Infra> estado=<publicado|preview> commit=<hash> medir_en=<AAAA-MM-DD> titulo="qué cambió" detalle="cómo y por qué, el resultado esperado"`.
Si descubriste una lección aplicable siempre: `bitacora.py aprende "regla corta" area=<área>`.


**Aprobaciones con botón (desde el 20-oct).** Antes de leer el hilo corre
`python3 scripts/agent/slack_bot.py approvals 14`: cada fila con `decision: "acepto"` equivale a un
"dale N" de Paola o Regina (el `id` es fecha-n de la propuesta y `n` el número); `no_por_ahora` se respeta y
se anota en el backlog como descartada por ahora. El "dale N" escrito en el hilo sigue valiendo como
respaldo. Si `approvals` falla (401/501), avisa en el hilo: falta METRICS_KEY o el proxy.

**Alertas de la Guardia (desde el 23-nov).** La Guardia publica "⚠️ *Guardia D de mes*" y a veces ofrece
algo "con tu dale". Nadie más lee esas respuestas: tú sí. `python3 scripts/agent/slack_bot.py read 80`,
toma los mensajes del bot Marina (`U0C83V7MHFA`) que empiecen con "Guardia" de los últimos 10 días y lee
con `thread <ts>` solo los que tengan respuestas. Un "dale" de Paola, Regina o Pepis ahí autoriza
exactamente lo que ese hilo ofreció en su última línea 🎯 (la alerta o, si ya contestaste con una
propuesta, tu propuesta), nada más:
- Si ofreció revisar o investigar: investiga con `/api/stats` (daily: pages, referrers, uniqueVisitors,
  languages, crawlers), el histórico de Clarity en `~/.config/kinedu-agent/history/` y `api/track.js`, y
  contesta en ese mismo hilo con lo encontrado (bloque 🔥 con el número clave y bloque 🎯 con qué hacer).
  Si hace falta un cambio al sitio o a cómo se cuentan las métricas, descríbelo ahí y pide "dale"; no lo
  construyas en esa corrida.
- Si ofreció un cambio concreto al sitio: flujo normal (directo si es técnico sin efecto visible, preview
  y "va" si se ve) y contesta en ese hilo.
- Si ofreció más de una cosa y el "dale" no dice cuál, pregunta con "❓ *Necesito tu decisión*" y no hagas nada.
- Un hilo está atendido cuando tu última respuesta es posterior al último mensaje de una aprobadora:
  no lo repitas. Anota en `decisiones.md`; el backlog solo cambia si tocaste el sitio.

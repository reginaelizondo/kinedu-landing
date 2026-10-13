# 03 · Implementador (martes a viernes 10:00)

Lee el hilo más reciente de recomendaciones en Slack #landing-agente. Solo actúa sobre
mensajes de Regina que digan "dale" con el número (o "dale todo"). Para cada aprobación:
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

# 06 · Guardia (diario 9:40)

Para el sitio, el formulario de contacto y el estado del último deploy corre **un solo
comando ya permitido**: `bash scripts/agent/guardia_check.sh` (no compongas curl ni `gh api`
con `$(...)` a mano, eso obliga a pedir permiso y traba la rutina).

Revisa que el sitio responda (home, /es, /pt, /blog, /masterclasses, /gift, webpromo), que
el último deploy no haya fallado, que el tráfico y las conversiones de ayer no caigan más de
30% contra los 7 días anteriores, que ningún A/B vaya más de 10% abajo con 500 vistas, y que
los errores de script en Clarity no se dupliquen. Si hay algo, un solo mensaje en Slack
"Guardia D de mes:". Si no hay nada, no escribe. Nunca cambia código.

Si la alerta vale la pena recordarla, déjala en la bitácora:
`python3 scripts/agent/bitacora.py add rol=Guardia tipo=alerta area=<área> estado=na titulo="qué pasó" detalle="..."`.

**Correos de Google Search Console (cuando Regina reenvíe uno).** Antes de alarmar, diagnostica:
- "Página con redirección" → casi siempre son nuestros 301 de consolidación. Verifica: el sitemap solo trae URLs destino; muestra ~40 URLs del sitemap, todas 200 (alguna en 301 = fuga, sacarla del sitemap); cruza con `vercel.json`. Si cuadra, es ruido bueno, no es la caída.
- "Página con errores 404" → cruza cada URL con su tráfico en GSC; 301 solo las que rankean/tienen enlaces, el resto se deja en 404.
- "Rastreada, no indexada" / "Alternativa con canónica" → suele ser contenido delgado o duplicado (ligar a la consolidación de series).
Siempre: reporta en Slack qué es, si es nuestro o de Google, y qué hacer (muchas veces nada). Anótalo en la bitácora.

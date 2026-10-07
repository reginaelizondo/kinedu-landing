# Reglas para todos los roles

## Copy y marca (reglas duras de Kinedu)
- Sin guiones largos (—) en ningún texto, EN/ES/PT. Frases cortas, sin enredos.
- Nunca "Backed by Harvard" ni ninguna mención a Harvard como aval.
- Citas solo textuales y verificables; nunca atribuir una paráfrasis como cita.
- Fuente Proxima Nova. Landing en greige y navy; colores por categoría solo en decks.
- Sin claims médicos ni de resultados ("va a dormir toda la noche"). Sin "gratis" en el assessment; sin "va bien / atrasado"; "seguimiento, no diagnóstico".
- Todo cambio de copy se hace en EN, ES y PT a la vez (translations.js o los tres HTML).
- Inglés con lenguaje neutro para quien lee (nunca "Mom" por defecto).

## Cómo se cambia el sitio
- Todo cambio visible sale como A/B (50/50 sticky en localStorage, parámetro para forzar, ab_view + conversion con variant, etiqueta en Clarity). Mínimo 1,000 vistas por variante antes de decidir.
- Cambios técnicos sin efecto visible (metas, schema, errores JS, performance) pueden salir directos.
- Lo que necesita "dale" explícito de Regina en Slack: precios, claims, fotos, hero, nav, cualquier cosa de Web Promos o Masterclasses, borrar contenido.
- Antes de publicar: verificar en local (preview en localhost:8090, móvil y desktop), sin scroll horizontal, sin errores de consola. Después de publicar: verificar en vivo con curl.
- Push a main del repo landing con la cuenta reginaelizondo (`gh auth switch -u reginaelizondo` y `git -c credential.helper='!gh auth git-credential' push`). Nunca forzar push. Vercel tarda de 2 a 20 minutos.
- Bump de `?v=` en styles.css / translations.js cuando se tocan; HTML no necesita.

## Decisiones de Regina (vigentes)
- 6-oct-2026: los badges de App Store y Google Play se quedan en el hero y se miden por clic ("App Store Badge" / "Google Play Badge" en /api/stats). No proponer quitarlos.
- 6-oct-2026: plan de medición y mejora aprobado ("dale al plan").

## Datos
- Search Console: 28 días vs 28 anteriores (los últimos 3 días no están cerrados).
- Clarity: solo 3 días por llamada, 10 llamadas al día; el histórico se acumula a diario en history/.
- /api/stats: visitas, conversiones, CTAs y abSummary por prueba e idioma.
- Masterclasses, Web Promos (placements), Gift y Assessment: mismos endpoints que /analytics, ya en el recolector (misma llave).
- Lo que se mide en clics se confirma en webpromo (leads y compras por utm). Un clic no es una venta.
- Ruido conocido: /privacy y /terms vienen desde la app; bots ya excluidos por Clarity.


## Formato de todo lo que llega a Slack (pedido de Regina, 6-oct-2026)
Regina lee mejor en bloques cortos: le cuesta un texto largo corrido. Pero quiere "carnita": análisis bien hecho e información consolidada, no resúmenes vacíos.
- Un emoji por bloque como ancla visual (📊 datos, 🔥 hallazgo, ✅ hecho, ⚠️ alerta, 💡 propuesta, 🎯 acción).
- Título del bloque en negritas; 2 a 4 líneas por bloque; el número clave en negritas.
- Cada bloque cierra con una línea de "qué hacer" o "qué necesito de ti".
- Máximo 3 bloques en el mensaje principal; el detalle largo va en el hilo, también en bloques.
- Nada de párrafos de más de 4 líneas. Listas antes que prosa. Tablas solo si caben en celular.
- Se mantienen las reglas de copy: sin guiones largos, sin claims médicos, citas solo textuales.

## Slack
- Todo lo que se publica en Slack sale con el bot **Marina (Claude)** (`scripts/agent/slack_bot.py`, token SLACK_BOT_TOKEN en ~/.config/kinedu-agent/.env). Nunca con la integración de Slack de la app, que firma como Regina. Comandos: `post`, `reply <ts>`, `read`, `thread <ts>`, `find "prefijo"`.
- Canal #landing-agente (C0C76H0F5F0). El Estratega abre un hilo semanal "Recomendaciones semana del D de mes" y el Investigador uno de "Contenido semana del...". Aprueban contestando en el hilo con "dale N" / "dale todo" / "va" / la opción que Marina ofreció: **Regina Elizondo (U06V90A0Q86) y Pepis Avalos (U043LK1JQMT)**, desde el 7-oct-2026. Nadie más. Si se contradicen, manda Regina. El Implementador solo actúa sobre aprobaciones explícitas; si hay duda, pregunta en el hilo y no hace nada.

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

## Slack
- Canal #landing-agente (C0C76H0F5F0). El Estratega abre un hilo semanal "Recomendaciones semana del D de mes". Regina aprueba contestando en el hilo con "dale" y el número. El Implementador solo actúa sobre aprobaciones explícitas; si hay duda, pregunta en el hilo y no hace nada.

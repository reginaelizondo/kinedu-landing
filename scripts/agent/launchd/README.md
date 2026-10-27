# Marina por launchd (desde 2026-10-27)

Las 7 rutinas del agente de la landing corren por **launchd**, sin depender de que la app de Claude
esté abierta, y en **modo acotado** (`claude -p --permission-mode acceptEdits` + allowlist; nunca
`--dangerously-skip-permissions`, decisión de Regina 27-oct). Esta carpeta es la copia versionada;
la copia viva está en `~/kinedu-landing-agent/schedule/` y los plists en `~/Library/LaunchAgents/`.

Por qué un clon en el home: launchd NO puede leer el contenido de archivos en ~/Desktop (TCC,
"Operation not permitted"; probado con una sonda el 27-oct). El agente trabaja en el clon
`~/kinedu-landing-agent/repo` (`git clone --local`, sparse-checkout sin blog-photos/blog-media/
Experts/Coaches: ~0 disco extra) y sincroniza con `origin/main` antes de cada rutina (falla ruidoso
en Slack si hay conflicto). Regina ve los commits del agente en su Desktop con `git pull`.

Horarios (hora local): diario 9:00 (Clarity histórico → Guardia) · lunes 9:30 (Medidor → Analista →
Estratega, secuencial) · mar-vie 10:00 Implementador · jueves 11:00 Investigador. Tope duro 60 min
por rutina (watchdog). Logs: `~/kinedu-landing-agent/schedule/logs/`.

Operación:
  pausar todo    for l in diario lunes impl jueves; do launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.kinedu.landing.$l.plist; done
  reanudar       for l in diario lunes impl jueves; do launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kinedu.landing.$l.plist; done
  correr una ya  ~/kinedu-landing-agent/schedule/run_routine.sh <id>   (ids = nombres en prompts/)
  estado         launchctl list | grep com.kinedu.landing   (PID "-" = armado, no corriendo)
Restaurar en otra Mac: copiar *.sh y prompts/ a ~/kinedu-landing-agent/schedule/, plists/ a
~/Library/LaunchAgents/, rehacer el clon y copiar .claude/settings.local.json al clon, luego "reanudar".
Las 7 tareas equivalentes de la app de Claude quedaron deshabilitadas (no borradas) el 27-oct.

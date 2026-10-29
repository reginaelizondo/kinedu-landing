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


## Modo acotado: allowlist que necesita el clon (29-oct)
Las rutinas corren con `--permission-mode acceptEdits` + el allowlist de `<clon>/.claude/settings.local.json`
(copiado del Desktop + reglas para git/gh/el python del venv/WebSearch). La validación por launchd del 29-oct
mostró que FALTAN dos reglas sin las que la Guardia y el Medidor quedan a medias (no pueden chequear URLs ni
comparar semanas):
- `Bash(curl:*)`  — chequeos de sitio y `/api/stats`
- `Read(/Users/reginaelizondo/.config/kinedu-agent/history/**)`  — comparar el weekly de la semana previa (NO el `.env`)
Agregarlas al `permissions.allow` del clon (lo bloquea el clasificador de auto-mode como "Self-Modification";
las agrega Regina o se autoriza una regla de `Bash`). Chrome headless/verificación visual queda fuera a propósito
(el Implementador degrada a verificación estática).

## Arreglos 29-oct (commit en este kit)
- **Modelo fijado a Sonnet** (`--model sonnet`): el default era Fable y su límite de uso tumbó el `clarity` del 29-oct (RC=1).
- **PATH exportado** en `run_routine.sh`: launchd arranca con PATH mínimo y `node` (/usr/local/bin) y `gh` (/opt/homebrew/bin) quedaban fuera.

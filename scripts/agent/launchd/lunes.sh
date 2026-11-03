#!/bin/zsh
# Lunes: genera el JSON semanal ANTES (weekly_pull tarda 3-5 min y la shell de Claude lo corta a 2),
# luego Medidor -> Analista -> Estratega, secuencial (orden garantizado).
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
S=/Users/reginaelizondo/kinedu-landing-agent/schedule/run_routine.sh
CLONE=/Users/reginaelizondo/kinedu-landing-agent/repo
PY=/Users/reginaelizondo/.config/kinedu-agent/venv/bin/python
LOG=/Users/reginaelizondo/kinedu-landing-agent/schedule/logs/weekly_pull-$(date +%Y%m%d).log
{
  echo "=== weekly_pull · $(date) ==="
  cd "$CLONE" && git fetch -q origin main && git pull --rebase -q origin main 2>&1 | tail -2
  "$PY" scripts/agent/weekly_pull.py 2>&1 | tail -5
  echo "=== fin weekly_pull · $(date) ==="
} >> "$LOG" 2>&1
"$S" landing-lunes-medidor
"$S" landing-lunes-analista
"$S" landing-lunes-estratega

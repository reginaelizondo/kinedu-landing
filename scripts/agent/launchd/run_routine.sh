#!/bin/zsh
# Corre UNA rutina de Marina headless desde el clon del home (TCC-safe), acotada.
# Uso: run_routine.sh <id-rutina>  (usa schedule/prompts/<id>.txt)
ID="$1"
BASE=/Users/reginaelizondo/kinedu-landing-agent
CLONE=$BASE/repo
SCHED=$BASE/schedule
PROMPT="$SCHED/prompts/$ID.txt"
PY=/Users/reginaelizondo/.config/kinedu-agent/venv/bin/python
CLAUDE=/Users/reginaelizondo/.local/bin/claude
LOG="$SCHED/logs/$ID-$(date +%Y%m%d-%H%M).log"
WATCHDOG=3600   # tope duro 60 min: no mas zombies
# launchd arranca con PATH minimo: node (/usr/local/bin) y gh (/opt/homebrew/bin) quedan fuera.
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

alert() { "$PY" "$CLONE/scripts/agent/slack_bot.py" post "$1" >/dev/null 2>&1 || true; }

{
  echo "=== $ID · $(date) ==="
  [ -f "$PROMPT" ] || { echo "sin prompt $PROMPT"; alert "Marina/$ID: no encontre el prompt."; exit 1; }

  net_ok() { curl -sI --max-time 6 https://api.github.com >/dev/null 2>&1; }
  t=0; until net_ok; do t=$((t+1)); [ $t -ge 6 ] && { echo "sin red, salto (no es error)"; exit 0; }; echo "sin red $t/6"; sleep 15; done

  cd "$CLONE" || { alert "Marina/$ID: no pude entrar al clon."; exit 1; }

  # Sincroniza con main: reintenta en cortes de red; distingue red (transitorio) de conflicto real.
  sync_ok=0
  for intento in 1 2 3; do
    if git fetch origin main --quiet 2>&1 && git pull --rebase origin main 2>&1; then sync_ok=1; break; fi
    git rebase --abort 2>/dev/null || true
    echo "sync intento $intento fallo; reintento en 20s"; sleep 20
  done
  if [ $sync_ok -ne 1 ]; then
    if git ls-files -u 2>/dev/null | grep -q .; then
      echo "CONFLICTO real de merge"; alert "Marina/$ID: CONFLICTO real de merge en el clon (hay archivos sin resolver). No corri; revisar a mano."
    else
      echo "sync fallo (posible red)"; alert "Marina/$ID: no pude sincronizar el clon con main (posible red caida). No corri; reintenta en la proxima corrida."
    fi
    exit 1
  fi

  "$CLAUDE" -p "$(cat "$PROMPT")" --model sonnet --permission-mode acceptEdits --max-turns 160 2>&1 &
  CPID=$!
  ( sleep $WATCHDOG; kill -TERM $CPID 2>/dev/null; sleep 10; kill -KILL $CPID 2>/dev/null ) &
  WPID=$!
  wait $CPID; RC=$?
  kill $WPID 2>/dev/null || true

  if [ $RC -ne 0 ]; then echo "claude RC=$RC"; alert "Marina/$ID: la rutina termino con error (codigo $RC) el $(date '+%a %H:%M')."
  else echo "OK rc=0"; fi
  echo "=== fin $ID · $(date) ==="
} >> "$LOG" 2>&1

#!/bin/bash
# Instala a Marina (el agente de la landing de Kinedu) en ESTA Mac.
#   bash scripts/agent/launchd/install.sh
# Requisitos previos (ver HANDOFF): Claude Code con sesion iniciada, gh con sesion y permiso de push al repo,
# y los secretos en ~/.config/kinedu-agent/ (.env + gsc-service-account.json). No instala nada si falta algo.
# Solo debe haber UNA Mac con Marina activa: dos instancias duplican mensajes en Slack y pushes.
# Prueba en seco (solo genera archivos en otra carpeta, sin clonar ni cargar launchd):
#   RENDER_ONLY=1 AGENT_HOME=/tmp/marina-test bash scripts/agent/launchd/install.sh
set -euo pipefail
OLD_HOME="/Users/reginaelizondo"                      # rutas con las que esta escrito el kit
KIT="$(cd "$(dirname "$0")" && pwd)"
AGENT_HOME="${AGENT_HOME:-$HOME/kinedu-landing-agent}"
CFG="$HOME/.config/kinedu-agent"
RENDER_ONLY="${RENDER_ONLY:-0}"
LA_DIR="$HOME/Library/LaunchAgents"; [ "$RENDER_ONLY" = "1" ] && LA_DIR="$AGENT_HOME/LaunchAgents"
REPO_URL="https://github.com/reginaelizondo/kinedu-landing.git"
say() { printf "\n== %s\n" "$1"; }
die() { printf "\nFALTA: %s\n" "$1"; exit 1; }

say "0. Requisitos"
for b in git curl python3; do command -v "$b" >/dev/null || die "$b no esta instalado"; done
CLAUDE_BIN="$(command -v claude || true)"
if [ "$RENDER_ONLY" != "1" ]; then
  [ -n "$CLAUDE_BIN" ] || die "Claude Code (comando 'claude'). Instalalo e inicia sesion."
  command -v gh >/dev/null || die "GitHub CLI (gh). brew install gh && gh auth login"
  GH_USER="${GH_USER:-$(gh api user -q .login)}"
  GIT_EMAIL="${GIT_EMAIL:-$(gh api user -q '"\(.id)+\(.login)@users.noreply.github.com"')}"
  [ -f "$CFG/.env" ] || die "$CFG/.env (pideselo a Regina por un canal seguro, nunca por Slack ni correo)"
  KEY="$(grep -E '^GSC_KEY_FILE=' "$CFG/.env" | cut -d= -f2- | sed "s#$OLD_HOME#$HOME#")"
  [ -f "$KEY" ] || die "la llave de Search Console en $KEY"
else
  CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"; GH_USER="${GH_USER:-tu-usuario}"; GIT_EMAIL="${GIT_EMAIL:-tu@correo}"
fi
echo "claude: $CLAUDE_BIN · GitHub: $GH_USER"

if [ "$RENDER_ONLY" != "1" ]; then
  say "1. Secretos: rutas de .env a esta Mac"
  sed -i '' "s#$OLD_HOME#$HOME#g" "$CFG/.env"; chmod 600 "$CFG/.env" "$KEY"

  say "2. Python del agente"
  [ -x "$CFG/venv/bin/python" ] || python3 -m venv "$CFG/venv"
  "$CFG/venv/bin/pip" -q install --upgrade requests google-auth
  mkdir -p "$CFG/history"

  say "3. Clon de trabajo del agente (ligero: sin historial de binarios ni carpetas de imagenes)"
  if [ ! -d "$AGENT_HOME/repo/.git" ]; then
    mkdir -p "$AGENT_HOME"
    git clone --filter=blob:none --no-checkout "$REPO_URL" "$AGENT_HOME/repo"
    git -C "$AGENT_HOME/repo" sparse-checkout set --no-cone '/*' '!/blog-photos' '!/blog-media' '!/Experts' '!/Coaches pictures'
    git -C "$AGENT_HOME/repo" checkout main
  fi
  git -C "$AGENT_HOME/repo" config user.name "$GH_USER"
  git -C "$AGENT_HOME/repo" config user.email "$GIT_EMAIL"
fi

say "4. Kit adaptado a esta Mac ($AGENT_HOME/schedule)"
S="$AGENT_HOME/schedule"; mkdir -p "$S/prompts" "$S/logs" "$LA_DIR"
conv() { sed -e "s#$OLD_HOME/.local/bin/claude#$CLAUDE_BIN#g" -e "s#$OLD_HOME/kinedu-landing-agent#$AGENT_HOME#g" -e "s#$OLD_HOME#$HOME#g" \
             -e "s#gh auth switch -u reginaelizondo#gh auth switch -u $GH_USER#g" -e "s#cuenta reginaelizondo#cuenta $GH_USER#g" "$1"; }
for f in run_routine.sh lunes.sh diario.sh impl.sh jueves.sh; do conv "$KIT/$f" > "$S/$f"; chmod +x "$S/$f"; done
for f in "$KIT"/prompts/*.txt; do conv "$f" > "$S/prompts/$(basename "$f")"; done
for f in "$KIT"/plists/*.plist; do conv "$f" > "$LA_DIR/$(basename "$f")"; done
LEFT="$( { grep -rl "$OLD_HOME" "$S" "$LA_DIR"/com.kinedu.landing.*.plist 2>/dev/null || true; } | wc -l | tr -d ' ')"
echo "archivos generados: $(ls "$S"/*.sh "$S"/prompts/*.txt "$LA_DIR"/com.kinedu.landing.*.plist | wc -l | tr -d ' ') · con rutas viejas: $LEFT"
[ "$LEFT" = "0" ] || die "quedaron rutas de la Mac original; no sigo"
[ "$RENDER_ONLY" = "1" ] && { say "Prueba en seco terminada (no se clono, no se cargo launchd)"; exit 0; }

say "5. Permisos del agente (decision tuya)"
P="$AGENT_HOME/repo/.claude/settings.local.json"
if [ ! -f "$P" ]; then
  echo "Marina corre sola, sin nadie que apruebe. Para trabajar necesita permiso de shell (git, curl, python) y leer su historico."
  echo "Sin esto corre pero casi no puede hacer nada. Es amplio: equivale a dejarla ejecutar comandos en esta Mac."
  read -r -p "Autorizas esos permisos para el agente en $AGENT_HOME/repo? [s/N] " ok
  if [ "$ok" = "s" ] || [ "$ok" = "S" ]; then
    mkdir -p "$(dirname "$P")"
    printf '{\n  "permissions": {\n    "allow": ["Bash", "Edit", "Write", "Read", "Glob", "Grep", "WebSearch", "WebFetch", "Read(%s/history/**)"]\n  }\n}\n' "$CFG" > "$P"
    echo "permisos escritos en $P"
  else echo "sin permisos: puedes crearlos despues (ver HANDOFF)"; fi
fi

say "6. Prueba de accesos"
( cd "$AGENT_HOME/repo" && "$CFG/venv/bin/python" scripts/agent/gsc_sitemaps.py | tail -1 ) || echo "Search Console fallo: revisa la llave"
( cd "$AGENT_HOME/repo" && "$CFG/venv/bin/python" scripts/agent/slack_bot.py read 1 | head -c 60; echo ) || echo "Slack fallo: revisa SLACK_BOT_TOKEN"
git -C "$AGENT_HOME/repo" push --dry-run origin main 2>&1 | tail -1 || echo "sin permiso de push: pide a Regina que te agregue como colaboradora"

say "7. Activar a Marina en esta Mac"
echo "Antes de decir que si: confirma con Regina que YA apago a Marina en su Mac (si no, corren dos)."
read -r -p "Cargar los 4 horarios en launchd ahora? [s/N] " go
if [ "$go" = "s" ] || [ "$go" = "S" ]; then
  for l in diario lunes impl jueves; do
    launchctl bootout "gui/$(id -u)" "$LA_DIR/com.kinedu.landing.$l.plist" 2>/dev/null || true
    launchctl bootstrap "gui/$(id -u)" "$LA_DIR/com.kinedu.landing.$l.plist" && echo "cargado: $l"
  done
  echo "Listo. Horarios: diario 9:00 · lunes 9:30 · mar-vie 10:00 · jueves 11:00. Logs en $S/logs/"
else echo "No se cargo. Cuando toque: vuelve a correr este script."; fi

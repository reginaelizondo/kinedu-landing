#!/usr/bin/env bash
# Chequeo de salud de la Guardia, en UN solo comando.
#
# Por qué existe: cuando la Guardia componía a mano `curl ... ; gh api .../$(git rev-parse ...)`,
# ese $(...) no se puede revisar antes de correr, así que Claude Code SIEMPRE pedía permiso y la
# rutina se trababa. Metido aquí, el $(...) vive dentro del script: la rutina corre un solo
# comando fijo (bash scripts/agent/guardia_check.sh), ya permitido, y no pregunta nada.
#
# Solo lee: códigos de estado del sitio, una validación del formulario de contacto (datos
# inválidos de prueba, no manda correo) y el estado del último deploy. No cambia nada.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || exit 1

echo "=== Sitio (código HTTP) ==="
for u in \
  https://www.kinedu.com/ \
  https://www.kinedu.com/es \
  https://www.kinedu.com/pt \
  https://www.kinedu.com/blog \
  https://www.kinedu.com/masterclasses \
  https://www.kinedu.com/gift \
  https://webpromo.kinedu.com/p/landing-kinedu ; do
  code=$(curl -s -o /dev/null -m 30 -w '%{http_code}' "$u")
  echo "  $code  $u"
done

echo "=== Formulario de contacto (validación, datos inválidos de prueba) ==="
code=$(curl -s -m 30 -o /dev/null -w '%{http_code}' -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"","email":"no-valido","message":"x"}' \
  https://www.kinedu.com/masterclasses/api/contact)
echo "  HTTP $code  (se espera 400: rechaza correo inválido)"

echo "=== Último deploy (estado del commit en main) ==="
git fetch origin -q 2>&1 | tail -2
head=$(git rev-parse origin/main)
state=$(gh api "repos/reginaelizondo/kinedu-landing/commits/${head}/status" --jq .state 2>/dev/null || echo "sin-dato")
echo "  main ${head:0:9} -> ${state}"

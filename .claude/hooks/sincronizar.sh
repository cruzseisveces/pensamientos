#!/usr/bin/env bash
# Commit y push de todo lo nuevo. Silencioso si no hay cambios.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
git add -A
git diff --cached --quiet && exit 0
git commit -q -m "diario: $(TZ=America/Argentina/Mendoza date '+%Y-%m-%d %H:%M')" || exit 0
git push -q 2>/dev/null || { git pull -q --rebase && git push -q; } || echo "No se pudo hacer push" >&2
exit 0

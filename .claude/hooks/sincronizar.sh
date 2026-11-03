#!/usr/bin/env bash
# Commit y push de todo lo nuevo, SIEMPRE a main (las sesiones en la nube trabajan en ramas claude/*).
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
python3 mapa/actualizar.py 2>/dev/null   # capa 1 del mapa, siempre
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "diario: $(TZ=America/Argentina/Mendoza date '+%Y-%m-%d %H:%M')" || exit 0
fi
git fetch -q origin main 2>/dev/null
if ! git rebase -q FETCH_HEAD 2>/dev/null; then
  git rebase --abort 2>/dev/null
  echo "Conflicto al sincronizar con main: avisale a Juan." >&2
  exit 0
fi
git push -q origin HEAD:main 2>/dev/null || { sleep 2; git push -q origin HEAD:main 2>/dev/null; } || echo "No se pudo hacer push a main: avisale a Juan." >&2
exit 0

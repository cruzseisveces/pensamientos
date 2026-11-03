#!/usr/bin/env bash
# Al empezar la sesión: traer lo último de main, aunque la sesión esté en otra rama.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
git fetch -q origin main 2>/dev/null && git rebase -q FETCH_HEAD 2>/dev/null || git rebase --abort 2>/dev/null
exit 0

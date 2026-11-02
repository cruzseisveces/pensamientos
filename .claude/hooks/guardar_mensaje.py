#!/usr/bin/env python3
"""Guarda cada mensaje de Juan, textual, en diario/AAAA-MM-DD.md."""
import json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

texto = data.get("prompt", "")
if not texto.strip():
    sys.exit(0)

raiz = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ahora = datetime.now(ZoneInfo("America/Argentina/Mendoza"))
carpeta = os.path.join(raiz, "diario")
os.makedirs(carpeta, exist_ok=True)
archivo = os.path.join(carpeta, ahora.strftime("%Y-%m-%d") + ".md")

nuevo = not os.path.exists(archivo)
with open(archivo, "a", encoding="utf-8") as f:
    if nuevo:
        f.write(f"# {ahora.strftime('%Y-%m-%d')}\n")
    f.write(f"\n## {ahora.strftime('%H:%M')}\n\n{texto.rstrip()}\n")
sys.exit(0)

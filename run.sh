#!/usr/bin/env bash
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { echo "Run  bash setup.sh  first."; exit 1; }
export PYTHONIOENCODING=utf-8
PORT=${1:-5000}
echo "Starting on http://localhost:$PORT   (Ctrl+C to stop)"
(command -v open >/dev/null && open "http://localhost:$PORT") || (command -v xdg-open >/dev/null && xdg-open "http://localhost:$PORT") || true
.venv/bin/python app.py "$PORT"

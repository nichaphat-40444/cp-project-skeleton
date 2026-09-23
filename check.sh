#!/usr/bin/env bash
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { echo "Run  bash setup.sh  first."; exit 1; }
export PYTHONIOENCODING=utf-8
.venv/bin/python check_project.py
echo; echo "--- pytest ---"
.venv/bin/python -m pytest -q

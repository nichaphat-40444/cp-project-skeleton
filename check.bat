@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (echo Run setup.bat first. & pause & exit /b 1)
set PYTHONIOENCODING=utf-8
".venv\Scripts\python.exe" check_project.py
echo.
echo --- pytest ---
".venv\Scripts\python.exe" -m pytest -q
pause

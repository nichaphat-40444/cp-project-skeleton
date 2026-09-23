@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (echo Run setup.bat first. & pause & exit /b 1)
set PYTHONIOENCODING=utf-8
set PORT=%1
if "%PORT%"=="" set PORT=5000
echo Starting on http://localhost:%PORT%   (Ctrl+C to stop)
start "" http://localhost:%PORT%
".venv\Scripts\python.exe" app.py %PORT%

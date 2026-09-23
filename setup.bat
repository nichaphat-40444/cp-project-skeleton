@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo === Computer Programming Project : setup ===
where python >nul 2>nul || (echo [!] python not found. Install Python 3.12+ from python.org and tick "Add python.exe to PATH". & pause & exit /b 1)
python -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)" || (echo [!] Python 3.11 or newer is required. & python --version & pause & exit /b 1)
if not exist .venv (
  echo [1/2] creating .venv ...
  python -m venv .venv || (echo [!] could not create .venv & pause & exit /b 1)
) else (
  echo [1/2] .venv already exists
)
echo [2/2] installing flask + pytest ...
".venv\Scripts\python.exe" -m pip install --quiet --no-index --find-links wheels -r requirements.txt 2>nul
if errorlevel 1 (
  echo     offline wheels did not match this Python - trying online ...
  ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt || (echo [!] install failed - check your internet connection & pause & exit /b 1)
)
".venv\Scripts\python.exe" -c "import flask, pytest; print('    flask', flask.__version__ if hasattr(flask,'__version__') else 'ok', '/ pytest', pytest.__version__)"
echo.
echo Done. Next:  run.bat   (opens the site)    check.bat   (score + tests)
pause

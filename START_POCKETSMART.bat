@echo off
setlocal
cd /d "%~dp0"
title PocketSmart AI - Launcher

echo ========================================
echo        PocketSmart AI - Starting
 echo ========================================
echo.
if not exist ".env" copy /Y ".env.example" ".env" >nul
if not exist ".venv\Scripts\python.exe" (
  echo First-time setup: creating Python environment...
  where py >nul 2>&1
  if %errorlevel%==0 (py -3 -m venv .venv) else (python -m venv .venv)
  if errorlevel 1 goto :error
)
echo Checking required packages...
.venv\Scripts\python.exe -m pip install -q -r requirements.txt
if errorlevel 1 goto :error
echo.
echo PocketSmart AI is starting...
echo Browser: http://127.0.0.1:8010
start "" "http://127.0.0.1:8010"
echo Keep this window open while using the website.
echo.
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8010
exit /b 0
:error
echo.
echo STARTUP FAILED.
pause
exit /b 1

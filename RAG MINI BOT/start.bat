@echo off
title NimbusNote RAG Bot Launcher
cd /d "%~dp0"

echo ===================================================
echo             NimbusNote RAG Mini Bot
echo ===================================================
echo.

:: 1. Check for virtual environment and create if missing
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Virtual environment not found. Creating .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Python is not installed or not in PATH. Please install Python 3.10+.
        pause
        exit /b 1
    )
    echo [INFO] Installing required dependencies...
    call .\.venv\Scripts\pip.exe install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
)

:: 2. Choose Mode
echo Select how you want to run the bot:
echo [1] Streamlit Web UI (Default / Browser)
echo [2] Terminal CLI (Console Chat)
echo.
set "choice=1"
set /p choice="Enter choice (1/2, default 1): "

if "%choice%"=="2" (
    echo.
    echo ===================================================
    echo Starting Terminal CLI...
    echo ===================================================
    call .\.venv\Scripts\python.exe cli.py
) else (
    echo.
    echo ===================================================
    echo Starting Streamlit Web UI...
    echo ===================================================
    call .\.venv\Scripts\streamlit.exe run app.py
)

echo.
pause

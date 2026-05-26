@echo off
REM My Python Buddy - Quick Start Script for Windows
REM This script sets up and runs the application

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   My Python Buddy - Startup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [INFO] Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Start the Flask backend
echo [INFO] Starting My Python Buddy backend server...
echo.
echo ========================================
echo   Backend Server Running
echo ========================================
echo.
echo  API Server: http://127.0.0.1:5000
echo  Frontend:   Open index.html in your browser
echo.
echo  Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause

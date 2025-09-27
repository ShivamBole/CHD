@echo off
REM CHD Prediction System - Development Startup Script for Windows
REM This script starts both backend and frontend servers for development

echo 🫀 Starting CHD Prediction System...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ All prerequisites found

REM Get the directory of this script
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Navigate to project root
cd /d "%PROJECT_ROOT%"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
cd backend
pip install -r requirements.txt

REM Check if model exists, if not train it
if not exist "data\model.pkl" (
    echo Model not found. Training model...
    python train_model.py
)

REM Start backend server in new window
echo 🚀 Starting backend server...
start "CHD Backend" cmd /k "python chd_prediction_api.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Navigate to frontend directory
cd ..\frontend

REM Install Node dependencies if needed
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

REM Start frontend server in new window
echo 🚀 Starting frontend server...
start "CHD Frontend" cmd /k "npm start"

echo ✅ CHD Prediction System is starting!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:5000
echo.
echo Press any key to exit this script (servers will continue running)
pause >nul


@echo off
echo 🚀 Starting CHD Prediction System
echo ================================

echo.
echo 📦 Installing React dependencies...
call npm install

echo.
echo 🔧 Starting Flask API server...
start "CHD API Server" cmd /k "python chd_prediction_api.py"

echo.
echo ⏳ Waiting for API to start...
timeout /t 5 /nobreak > nul

echo.
echo 🌐 Starting React development server...
echo.
echo ✅ System is starting up!
echo 📱 React app will open at: http://localhost:3000
echo 🔗 API server running at: http://localhost:5000
echo.

call npm start
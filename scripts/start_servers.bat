@echo off
echo 🚀 Starting CHD Prediction System
echo ================================

echo.
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 🔧 Starting Flask API server...
start "CHD API Server" cmd /k "python chd_prediction_api.py"

echo.
echo ⏳ Waiting for API to start...
timeout /t 5 /nobreak > nul

echo.
echo 📦 Installing React dependencies...
call npm install

echo.
echo 🌐 Starting React development server...
echo.
echo ✅ System is starting up!
echo 📱 React app will open at: http://localhost:3000
echo 🔗 API server running at: http://localhost:5000
echo.
echo 💡 If you get "Failed to fetch" error:
echo    1. Make sure both servers are running
echo    2. Check that port 5000 is not blocked
echo    3. Try refreshing the React app
echo.

call npm start
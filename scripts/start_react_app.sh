#!/bin/bash

echo "🚀 Starting CHD Prediction System"
echo "================================"

echo ""
echo "📦 Installing React dependencies..."
npm install

echo ""
echo "🔧 Starting Flask API server in background..."
python chd_prediction_api.py &
API_PID=$!

echo ""
echo "⏳ Waiting for API to start..."
sleep 5

echo ""
echo "🌐 Starting React development server..."
echo ""
echo "✅ System is starting up!"
echo "📱 React app will open at: http://localhost:3000"
echo "🔗 API server running at: http://localhost:5000"
echo ""

# Start React app
npm start

# Cleanup function
cleanup() {
    echo "🛑 Shutting down..."
    kill $API_PID 2>/dev/null
    exit
}

# Set trap to cleanup on exit
trap cleanup EXIT
#!/usr/bin/env python3
"""
Check if both servers are running
"""

import requests
import time
import webbrowser

def check_api_server():
    """Check if Flask API is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=3)
        if response.status_code == 200:
            print("✅ Flask API Server: RUNNING")
            print(f"   Status: {response.json()['status']}")
            print(f"   Model Loaded: {response.json()['model_loaded']}")
            return True
        else:
            print("❌ Flask API Server: NOT RESPONDING")
            return False
    except Exception as e:
        print("❌ Flask API Server: NOT RUNNING")
        print(f"   Error: {e}")
        return False

def check_react_server():
    """Check if React server is running"""
    try:
        response = requests.get('http://localhost:3000', timeout=3)
        if response.status_code == 200:
            print("✅ React Server: RUNNING")
            return True
        else:
            print("❌ React Server: NOT RESPONDING")
            return False
    except Exception as e:
        print("❌ React Server: NOT RUNNING")
        print(f"   Error: {e}")
        return False

def main():
    print("🚀 CHD Prediction System Status Check")
    print("=" * 50)
    
    api_running = check_api_server()
    react_running = check_react_server()
    
    print("\n" + "=" * 50)
    print("📊 SYSTEM STATUS")
    print("=" * 50)
    
    if api_running and react_running:
        print("🎉 BOTH SERVERS ARE RUNNING!")
        print("\n🌐 Access your application:")
        print("   React App: http://localhost:3000")
        print("   API Server: http://localhost:5000")
        print("\n💡 You can now:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Fill out the patient form")
        print("   3. Get CHD risk predictions!")
        
        # Open browser automatically
        print("\n🔗 Opening React app in browser...")
        webbrowser.open('http://localhost:3000')
        
    elif api_running and not react_running:
        print("⚠️  API is running but React server is not")
        print("💡 Start React server with: npm start")
        
    elif not api_running and react_running:
        print("⚠️  React is running but API server is not")
        print("💡 Start API server with: python chd_prediction_api.py")
        
    else:
        print("❌ BOTH SERVERS ARE NOT RUNNING")
        print("\n🔧 To start the system:")
        print("   1. Start API: python chd_prediction_api.py")
        print("   2. Start React: npm start")
        print("   3. Or use: start_servers.bat")

if __name__ == "__main__":
    main()
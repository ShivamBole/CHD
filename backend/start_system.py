#!/usr/bin/env python3
"""
CHD Prediction System Startup Script
Automatically sets up and starts the CHD prediction system
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'chd_prediction_api.py',
        'train_model.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files found")
    return True

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_dataset():
    """Check if dataset exists"""
    if not os.path.exists('data_cardiovascular_risk.csv'):
        print("❌ Dataset file 'data_cardiovascular_risk.csv' not found")
        print("Please download the cardiovascular dataset and place it in the project root")
        return False
    
    print("✅ Dataset found")
    return True

def train_model():
    """Train the ML model"""
    print("🤖 Training ML model...")
    try:
        result = subprocess.run([sys.executable, 'train_model.py'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Model trained successfully")
            return True
        else:
            print(f"❌ Model training failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Model training error: {e}")
        return False

def start_api_server():
    """Start the API server"""
    print("🚀 Starting API server...")
    try:
        # Start the API server in background
        process = subprocess.Popen([sys.executable, 'chd_prediction_api.py'])
        
        # Wait for server to start
        print("⏳ Waiting for API server to start...")
        time.sleep(5)
        
        # Test if server is running
        try:
            response = requests.get('http://localhost:5000/health', timeout=5)
            if response.status_code == 200:
                print("✅ API server started successfully")
                print("🌐 API available at: http://localhost:5000")
                return process
            else:
                print("❌ API server not responding correctly")
                return None
        except requests.exceptions.RequestException:
            print("❌ API server not responding")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def run_tests():
    """Run API tests"""
    print("🧪 Running API tests...")
    try:
        result = subprocess.run([sys.executable, 'test_api.py'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed")
            print(result.stdout)
        else:
            print("❌ Some tests failed")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Test execution error: {e}")

def main():
    """Main startup function"""
    print("🫀 CHD Prediction System Startup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check dataset
    if not check_dataset():
        print("\n📋 To get the dataset:")
        print("1. Download the cardiovascular dataset")
        print("2. Place it as 'data_cardiovascular_risk.csv' in the project root")
        print("3. Run this script again")
        sys.exit(1)
    
    # Train model
    if not train_model():
        sys.exit(1)
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        sys.exit(1)
    
    # Run tests
    run_tests()
    
    print("\n" + "=" * 50)
    print("🎉 CHD Prediction System is ready!")
    print("\n📋 Next steps:")
    print("1. API Server: http://localhost:5000")
    print("2. Health Check: http://localhost:5000/health")
    print("3. Use the React component in your frontend")
    print("4. Check README.md for detailed integration guide")
    
    print("\n🛑 To stop the system, press Ctrl+C")
    
    try:
        # Keep the script running
        api_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        api_process.terminate()
        print("✅ System stopped")

if __name__ == "__main__":
    main()
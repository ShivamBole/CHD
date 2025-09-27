#!/usr/bin/env python3
"""
Test API connection and fix CORS issues
"""

import requests
import json

def test_api_connection():
    """Test if the API is accessible"""
    try:
        # Test health endpoint
        print("🔍 Testing API connection...")
        response = requests.get('http://localhost:5000/health', timeout=5)
        
        if response.status_code == 200:
            print("✅ API is running and accessible")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the Flask server running?")
        print("💡 Start the API with: python chd_prediction_api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction_endpoint():
    """Test the prediction endpoint"""
    test_data = {
        "age": 45,
        "education": "2",
        "sex": "M",
        "is_smoking": "NO",
        "cigsPerDay": "0",
        "BPMeds": "NO",
        "prevalentStroke": "NO",
        "prevalentHyp": "NO",
        "diabetes": "NO",
        "totChol": 200,
        "sysBP": 120,
        "diaBP": 80,
        "BMI": 25.0,
        "heartRate": 75,
        "glucose": 85
    }
    
    try:
        print("\n🧪 Testing prediction endpoint...")
        response = requests.post(
            'http://localhost:5000/predict', 
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction endpoint working!")
            print(f"Risk Level: {result['risk_level']}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CHD Prediction API Connection Test")
    print("=" * 40)
    
    if test_api_connection():
        test_prediction_endpoint()
    else:
        print("\n💡 Solutions:")
        print("1. Make sure Flask API is running: python chd_prediction_api.py")
        print("2. Check if port 5000 is available")
        print("3. Try restarting the API server")
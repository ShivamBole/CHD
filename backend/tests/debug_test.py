#!/usr/bin/env python3
"""
Debug test for API issues
"""

import requests
import json

def test_simple_prediction():
    """Test with very simple data"""
    print("🔍 Testing Simple Prediction...")
    
    simple_data = {
        "age": 50,
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
        "glucose": 90
    }
    
    try:
        response = requests.post('http://localhost:5000/predict', json=simple_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Simple prediction successful!")
            print(f"Risk Level: {result['risk_level']}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health...")
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check successful!")
            print(f"Status: {result['status']}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🧪 DEBUG API TESTING")
    print("=" * 30)
    
    test_health()
    test_simple_prediction()
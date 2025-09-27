#!/usr/bin/env python3
"""
Test script for CHD Prediction API
Tests the API endpoints and functionality
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_prediction():
    """Test the prediction endpoint"""
    print("\nTesting prediction endpoint...")
    
    # Sample patient data
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
        "BMI": 25.5,
        "heartRate": 75,
        "glucose": 85
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data)
        if response.status_code == 200:
            print("✅ Prediction test passed")
            result = response.json()
            print(f"Risk Level: {result['risk_level']}")
            print(f"CHD Probability: {result['probability']['chd']:.2%}")
            print(f"Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            print(f"Has Visualization: {'Yes' if result['visualization'] else 'No'}")
        else:
            print(f"❌ Prediction test failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Prediction test error: {e}")

def test_high_risk_prediction():
    """Test with high-risk patient data"""
    print("\nTesting high-risk prediction...")
    
    high_risk_data = {
        "age": 65,
        "education": "1",
        "sex": "M",
        "is_smoking": "YES",
        "cigsPerDay": "20",
        "BPMeds": "YES",
        "prevalentStroke": "NO",
        "prevalentHyp": "YES",
        "diabetes": "YES",
        "totChol": 280,
        "sysBP": 160,
        "diaBP": 95,
        "BMI": 32.5,
        "heartRate": 95,
        "glucose": 150
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=high_risk_data)
        if response.status_code == 200:
            print("✅ High-risk prediction test passed")
            result = response.json()
            print(f"Risk Level: {result['risk_level']}")
            print(f"CHD Probability: {result['probability']['chd']:.2%}")
            print(f"Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            print(f"Recommendations: {len(result['recommendations'])}")
        else:
            print(f"❌ High-risk prediction test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ High-risk prediction test error: {e}")

def test_analyze_endpoint():
    """Test the analyze endpoint"""
    print("\nTesting analyze endpoint...")
    
    test_data = {
        "age": 50,
        "education": "3",
        "sex": "F",
        "is_smoking": "NO",
        "cigsPerDay": "0",
        "BPMeds": "NO",
        "prevalentStroke": "NO",
        "prevalentHyp": "NO",
        "diabetes": "NO",
        "totChol": 180,
        "sysBP": 110,
        "diaBP": 70,
        "BMI": 23.5,
        "heartRate": 65,
        "glucose": 90
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=test_data)
        if response.status_code == 200:
            print("✅ Analyze test passed")
            result = response.json()
            print(f"Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            print(f"Has Visualization: {'Yes' if result['visualization'] else 'No'}")
        else:
            print(f"❌ Analyze test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Analyze test error: {e}")

def main():
    """Run all tests"""
    print("🧪 CHD Prediction API Test Suite")
    print("=" * 50)
    
    # Wait a moment for API to be ready
    print("Waiting for API to be ready...")
    time.sleep(2)
    
    # Run tests
    test_health_check()
    test_prediction()
    test_high_risk_prediction()
    test_analyze_endpoint()
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")

if __name__ == "__main__":
    main()
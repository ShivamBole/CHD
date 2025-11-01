"""
Test script for the CHD Prediction API
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_single_prediction():
    """Test single prediction endpoint"""
    print("Testing single prediction...")
    
    # Sample patient data with categorical strings
    patient_data = {
        "age": 55,
        "education": 2,
        "sex": "M",  # M for Male
        "is_smoking": "YES",  # YES for smoking
        "cigsPerDay": 20,
        "BPMeds": "NO",
        "prevalentStroke": "NO",
        "prevalentHyp": "YES",
        "diabetes": "NO",
        "totChol": 220,
        "sysBP": 140,
        "diaBP": 90,
        "BMI": 28,
        "heartRate": 75,
        "glucose": 85
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=patient_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("Testing batch prediction...")
    
    # Multiple patients with categorical strings
    batch_data = {
        "patients": [
            {
                "age": 55,
                "education": 2,
                "sex": "M",
                "is_smoking": "YES",
                "cigsPerDay": 20,
                "BPMeds": "NO",
                "prevalentStroke": "NO",
                "prevalentHyp": "YES",
                "diabetes": "NO",
                "totChol": 220,
                "sysBP": 140,
                "diaBP": 90,
                "BMI": 28,
                "heartRate": 75,
                "glucose": 85
            },
            {
                "age": 45,
                "education": 3,
                "sex": "F",
                "is_smoking": "NO",
                "cigsPerDay": 0,
                "BPMeds": "NO",
                "prevalentStroke": "NO",
                "prevalentHyp": "NO",
                "diabetes": "NO",
                "totChol": 180,
                "sysBP": 120,
                "diaBP": 80,
                "BMI": 22,
                "heartRate": 70,
                "glucose": 75
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/predict/batch", json=batch_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_model_info():
    """Test model info endpoint"""
    print("Testing model info...")
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


if __name__ == "__main__":
    print("="*70)
    print("CHD Prediction API - Test Script")
    print("="*70)
    print()
    
    try:
        # Test all endpoints
        test_health_check()
        test_single_prediction()
        test_batch_prediction()
        test_model_info()
        
        print("="*70)
        print("✅ All tests completed successfully!")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the API is running: python api.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


#!/usr/bin/env python3
"""
Quick test for API status
"""

import requests
import time

def quick_test():
    """Quick test of the main functionality"""
    print("🚀 QUICK API STATUS CHECK")
    print("=" * 40)
    
    # Test data
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
        # Test health
        print("🔍 Testing Health Endpoint...")
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            print("✅ Health Check: PASS")
        else:
            print("❌ Health Check: FAIL")
            return False
            
        # Test prediction
        print("🎯 Testing Prediction Endpoint...")
        pred_response = requests.post('http://localhost:5000/predict', json=test_data, timeout=10)
        if pred_response.status_code == 200:
            result = pred_response.json()
            print("✅ Prediction: PASS")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   CHD Probability: {result['probability']['chd']:.2%}")
            print(f"   Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            return True
        else:
            print(f"❌ Prediction: FAIL ({pred_response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Server too slow")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    print("\n" + "=" * 40)
    if success:
        print("🎉 CORE APIS ARE WORKING!")
        print("✅ Health endpoint: Working")
        print("✅ Prediction endpoint: Working")
        print("📊 Ready for React integration!")
    else:
        print("⚠️  Some issues detected")
        print("💡 Try restarting the server")
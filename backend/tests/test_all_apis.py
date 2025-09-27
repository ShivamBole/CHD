#!/usr/bin/env python3
"""
Comprehensive test for all CHD Prediction API endpoints
"""

import requests
import json

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health Check: {result['status']}")
            print(f"📊 Model Loaded: {result['model_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_prediction_endpoint():
    """Test the prediction endpoint"""
    print("\n🎯 Testing Prediction Endpoint...")
    
    # Low risk patient
    low_risk_data = {
        "age": 35,
        "education": "4",
        "sex": "F",
        "is_smoking": "NO",
        "cigsPerDay": "0",
        "BPMeds": "NO",
        "prevalentStroke": "NO",
        "prevalentHyp": "NO",
        "diabetes": "NO",
        "totChol": 150,
        "sysBP": 110,
        "diaBP": 70,
        "BMI": 22.0,
        "heartRate": 65,
        "glucose": 80
    }
    
    try:
        response = requests.post('http://localhost:5000/predict', json=low_risk_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Low Risk Prediction: {result['risk_level']}")
            print(f"📈 CHD Probability: {result['probability']['chd']:.2%}")
            print(f"⚠️  Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_high_risk_prediction():
    """Test with high risk patient data"""
    print("\n🚨 Testing High Risk Prediction...")
    
    # High risk patient
    high_risk_data = {
        "age": 70,
        "education": "1",
        "sex": "M",
        "is_smoking": "YES",
        "cigsPerDay": "25",
        "BPMeds": "YES",
        "prevalentStroke": "YES",
        "prevalentHyp": "YES",
        "diabetes": "YES",
        "totChol": 300,
        "sysBP": 180,
        "diaBP": 100,
        "BMI": 35.0,
        "heartRate": 110,
        "glucose": 200
    }
    
    try:
        response = requests.post('http://localhost:5000/predict', json=high_risk_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ High Risk Prediction: {result['risk_level']}")
            print(f"📈 CHD Probability: {result['probability']['chd']:.2%}")
            print(f"⚠️  Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            
            if result['risk_analysis']['risk_factors']:
                print("🚨 High Risk Factors:")
                for factor in result['risk_analysis']['risk_factors'][:5]:  # Show first 5
                    print(f"   • {factor['feature']}: {factor['value']} ({factor['normal_range']})")
            
            return True
        else:
            print(f"❌ High risk prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ High risk prediction error: {e}")
        return False

def test_analyze_endpoint():
    """Test the analyze endpoint"""
    print("\n📊 Testing Analyze Endpoint...")
    
    analyze_data = {
        "age": 60,
        "education": "2",
        "sex": "M",
        "is_smoking": "YES",
        "cigsPerDay": "15",
        "BPMeds": "YES",
        "prevalentStroke": "NO",
        "prevalentHyp": "YES",
        "diabetes": "NO",
        "totChol": 250,
        "sysBP": 150,
        "diaBP": 90,
        "BMI": 28.5,
        "heartRate": 85,
        "glucose": 120
    }
    
    try:
        response = requests.post('http://localhost:5000/analyze', json=analyze_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis completed")
            print(f"📊 Total Risk Factors: {result['total_risk_factors']}")
            print(f"📈 Total Normal Values: {result['total_normal_values']}")
            
            if result['risk_factors']:
                print("🚨 Risk Factors Found:")
                for factor in result['risk_factors'][:3]:  # Show first 3
                    print(f"   • {factor['feature']}: {factor['value']} - {factor['status']}")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🧪 COMPREHENSIVE API TESTING")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Prediction (Low Risk)", test_prediction_endpoint),
        ("Prediction (High Risk)", test_high_risk_prediction),
        ("Analysis", test_analyze_endpoint)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 ALL APIs ARE WORKING PERFECTLY!")
    else:
        print("⚠️  Some APIs need attention")

if __name__ == "__main__":
    main()
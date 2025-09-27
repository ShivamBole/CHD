#!/usr/bin/env python3
"""
Simple test for CHD Prediction API
"""

import requests
import json

def test_prediction():
    """Test the prediction endpoint with sample data"""
    
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
        print("🧪 Testing CHD Prediction API...")
        print("📊 Sample Patient Data:")
        for key, value in test_data.items():
            print(f"   {key}: {value}")
        
        print("\n🔄 Making prediction request...")
        response = requests.post('http://localhost:5000/predict', json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ Prediction Successful!")
            print(f"🎯 Risk Level: {result['risk_level']}")
            print(f"📈 CHD Probability: {result['probability']['chd']:.2%}")
            print(f"📉 No CHD Probability: {result['probability']['no_chd']:.2%}")
            print(f"⚠️  Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            
            if result['risk_analysis']['risk_factors']:
                print("\n🚨 Risk Factors Detected:")
                for factor in result['risk_analysis']['risk_factors']:
                    print(f"   • {factor['feature']}: {factor['value']} ({factor['normal_range']}) - {factor['status']}")
            else:
                print("\n✅ No Risk Factors - All values within normal range!")
            
            if result['recommendations']:
                print(f"\n💡 Health Recommendations ({len(result['recommendations'])}):")
                for i, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"   {i}. {rec['title']}: {rec['message']}")
            
            print(f"\n📊 Visualization: {'Available' if result['visualization'] else 'Not available'}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure the API server is running on http://localhost:5000")

if __name__ == "__main__":
    test_prediction()
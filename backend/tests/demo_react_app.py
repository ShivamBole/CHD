#!/usr/bin/env python3
"""
Demo script to test the React CHD Prediction App
"""

import requests
import json
import time
import webbrowser
from threading import Timer

def test_api_connection():
    """Test if the API is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ API Server is running")
            return True
        else:
            print("❌ API Server not responding")
            return False
    except Exception as e:
        print(f"❌ API Connection failed: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint with sample data"""
    sample_data = {
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
        print("🧪 Testing prediction with sample data...")
        response = requests.post('http://localhost:5000/predict', json=sample_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful!")
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   CHD Probability: {result['probability']['chd']:.2%}")
            print(f"   Risk Factors: {result['risk_analysis']['total_risk_factors']}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def open_react_app():
    """Open the React app in browser"""
    print("🌐 Opening React app in browser...")
    webbrowser.open('http://localhost:3000')

def main():
    """Main demo function"""
    print("🚀 CHD Prediction React App Demo")
    print("=" * 40)
    
    # Test API connection
    if not test_api_connection():
        print("\n❌ Please start the Flask API first:")
        print("   python chd_prediction_api.py")
        return
    
    # Test prediction
    if not test_prediction():
        print("\n❌ API prediction test failed")
        return
    
    print("\n✅ All API tests passed!")
    print("\n📱 React App Demo Instructions:")
    print("1. The React app should be running at http://localhost:3000")
    print("2. If not, run: npm start")
    print("3. Fill out the patient form with health data")
    print("4. Click 'Get Risk Assessment' to see results")
    print("5. View interactive charts and recommendations")
    
    # Open browser after a delay
    Timer(2.0, open_react_app).start()
    
    print("\n🎯 Demo Features to Test:")
    print("• Patient form with all health metrics")
    print("• Real-time risk prediction")
    print("• Interactive visualizations")
    print("• Risk factor analysis")
    print("• Personalized recommendations")
    print("• Responsive design (try mobile view)")
    
    print("\n💡 Sample Test Data:")
    print("   Age: 45, Sex: Male, Non-smoker")
    print("   Cholesterol: 200, BP: 120/80")
    print("   BMI: 25.0, Heart Rate: 75")
    print("   Glucose: 85")

if __name__ == "__main__":
    main()
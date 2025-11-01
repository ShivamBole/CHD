"""
Test script to verify risk level classification with the new thresholds
"""

import requests
import json
import pandas as pd

# API base URL
BASE_URL = "http://localhost:8000"

def test_risk_levels():
    """Test risk level classification for different patient profiles"""
    print("\n=== TESTING RISK LEVEL CLASSIFICATION ===\n")
    
    # Test cases for different risk levels
    test_cases = [
        {
            "name": "HIGH RISK CASE",
            "data": {
                "age": 65,
                "education": 1,
                "sex": "M",
                "is_smoking": "YES",
                "cigsPerDay": 30,
                "BPMeds": "YES",
                "prevalentStroke": "YES",
                "prevalentHyp": "YES",
                "diabetes": "YES",
                "totChol": 280,
                "sysBP": 180,
                "diaBP": 110,
                "BMI": 32,
                "heartRate": 88,
                "glucose": 130
            },
            "expected_risk": "HIGH RISK"
        },
        {
            "name": "MEDIUM RISK CASE",
            "data": {
                "age": 50,
                "education": 3,
                "sex": "F",
                "is_smoking": "YES",
                "cigsPerDay": 10,
                "BPMeds": "NO",
                "prevalentStroke": "NO",
                "prevalentHyp": "NO",
                "diabetes": "NO",
                "totChol": 200,
                "sysBP": 130,
                "diaBP": 85,
                "BMI": 26,
                "heartRate": 72,
                "glucose": 90
            },
            "expected_risk": "MEDIUM RISK"
        },
        {
            "name": "LOW RISK CASE",
            "data": {
                "age": 40,
                "education": 4,
                "sex": "F",
                "is_smoking": "NO",
                "cigsPerDay": 0,
                "BPMeds": "NO",
                "prevalentStroke": "NO",
                "prevalentHyp": "NO",
                "diabetes": "NO",
                "totChol": 170,
                "sysBP": 110,
                "diaBP": 70,
                "BMI": 22,
                "heartRate": 65,
                "glucose": 80
            },
            "expected_risk": "LOW RISK"
        }
    ]
    
    results = []
    
    # Test each case
    for case in test_cases:
        print(f"Testing {case['name']}...")
        response = requests.post(f"{BASE_URL}/predict", json=case['data'])
        
        if response.status_code == 200:
            result = response.json()
            actual_risk = result.get('risk_level', 'UNKNOWN')
            # Remove " Risk" suffix if present
            if actual_risk.endswith(" Risk"):
                actual_risk = actual_risk[:-5]
            probability = result.get('disease_probability', 0)
            
            status = "PASS" if actual_risk == case['expected_risk'] else "FAIL"
            
            print(f"Expected: {case['expected_risk']}")
            print(f"Actual: {actual_risk}")
            print(f"Probability: {probability}")
            print(f"Status: {status}")
            print()
            
            results.append({
                "case": case['name'],
                "expected_risk": case['expected_risk'],
                "actual_risk": actual_risk,
                "probability": probability,
                "status": status
            })
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            print()
    
    # Save results to file
    with open('risk_level_test_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    # Print summary
    print("\n=== TEST SUMMARY ===")
    passed = sum(1 for r in results if r['status'] == 'PASS')
    total = len(results)
    print(f"Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("All tests passed! Risk level classification is working correctly.")
    else:
        print("Some tests failed. Please check the results.")

if __name__ == "__main__":
    test_risk_levels()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHD Prediction API
Flask API for Cardiovascular Disease Risk Prediction
"""

import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for model components
model = None
scaler = None
feature_columns = None

def load_model():
    """Load the trained model and scaler"""
    global model, scaler, feature_columns
    
    try:
        # Load model
        with open('data/model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Load scaler
        with open('data/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        # Load feature columns
        with open('data/feature_columns.pkl', 'rb') as f:
            feature_columns = pickle.load(f)
        
        logger.info("Model loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

def preprocess_input(data):
    """Preprocess input data for prediction"""
    try:
        # Create DataFrame from input data
        df = pd.DataFrame([data])
        
        # Handle categorical variables
        categorical_mappings = {
            'sex': {'M': 1, 'F': 0},
            'is_smoking': {'YES': 1, 'NO': 0},
            'BPMeds': {'YES': 1, 'NO': 0},
            'prevalentStroke': {'YES': 1, 'NO': 0},
            'prevalentHyp': {'YES': 1, 'NO': 0},
            'diabetes': {'YES': 1, 'NO': 0}
        }
        
        for col, mapping in categorical_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)
        
        # Convert education to numeric
        if 'education' in df.columns:
            df['education'] = pd.to_numeric(df['education'], errors='coerce')
        
        # Convert other numeric fields
        numeric_fields = ['age', 'cigsPerDay', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors='coerce')
        
        # Select only the required features in the correct order
        processed_data = df[feature_columns].fillna(0)
        
        return processed_data.values
        
    except Exception as e:
        logger.error(f"Error preprocessing input: {e}")
        return None

def analyze_risk_factors(data):
    """Analyze risk factors in the input data"""
    risk_factors = []
    normal_ranges = {
        'age': (18, 65),
        'totChol': (0, 200),
        'sysBP': (90, 140),
        'diaBP': (60, 90),
        'BMI': (18.5, 24.9),
        'heartRate': (60, 100),
        'glucose': (70, 100)
    }
    
    # Check each risk factor
    for feature, (min_val, max_val) in normal_ranges.items():
        if feature in data:
            value = float(data[feature])
            if value < min_val or value > max_val:
                risk_factors.append({
                    'feature': feature,
                    'value': value,
                    'normal_range': f"{min_val}-{max_val}",
                    'status': 'High' if value > max_val else 'Low'
                })
    
    # Check categorical risk factors
    if data.get('is_smoking') == 'YES':
        risk_factors.append({
            'feature': 'smoking',
            'value': 'Yes',
            'normal_range': 'No',
            'status': 'High'
        })
    
    if data.get('diabetes') == 'YES':
        risk_factors.append({
            'feature': 'diabetes',
            'value': 'Yes',
            'normal_range': 'No',
            'status': 'High'
        })
    
    if data.get('prevalentHyp') == 'YES':
        risk_factors.append({
            'feature': 'hypertension',
            'value': 'Yes',
            'normal_range': 'No',
            'status': 'High'
        })
    
    return risk_factors

def generate_recommendations(risk_factors, risk_level, data=None):
    """Generate health recommendations based on risk factors and current health status"""
    recommendations = []
    
    if risk_level == 'High':
        recommendations.extend([
            {
                'title': 'Immediate Medical Consultation',
                'message': 'Please consult with a healthcare provider immediately for comprehensive cardiovascular assessment.',
                'priority': 'urgent'
            },
            {
                'title': 'Lifestyle Changes',
                'message': 'Focus on diet, exercise, and stress management under medical supervision.',
                'priority': 'high'
            }
        ])
    elif risk_level == 'Low':
        # Preventive recommendations for low-risk patients
        recommendations.extend([
            {
                'title': 'Maintain Current Health Status',
                'message': 'Congratulations! Your current health profile shows low risk for heart disease. Continue maintaining your healthy lifestyle.',
                'priority': 'maintenance'
            },
            {
                'title': 'Regular Health Monitoring',
                'message': 'Schedule annual health checkups to monitor your cardiovascular health and catch any changes early.',
                'priority': 'preventive'
            }
        ])
    
    # Specific recommendations based on risk factors
    for factor in risk_factors:
        if factor['feature'] == 'smoking':
            recommendations.append({
                'title': 'Quit Smoking',
                'message': 'Smoking significantly increases cardiovascular risk. Consider smoking cessation programs.',
                'priority': 'high'
            })
        elif factor['feature'] == 'BMI':
            if factor['status'] == 'High':
                recommendations.append({
                    'title': 'Weight Management',
                    'message': 'Maintain a healthy weight through balanced diet and regular exercise.',
                    'priority': 'medium'
                })
        elif factor['feature'] == 'sysBP' or factor['feature'] == 'diaBP':
            recommendations.append({
                'title': 'Blood Pressure Management',
                'message': 'Monitor blood pressure regularly and follow medical advice for hypertension management.',
                'priority': 'high'
            })
        elif factor['feature'] == 'totChol':
            recommendations.append({
                'title': 'Cholesterol Management',
                'message': 'Follow a heart-healthy diet and consider cholesterol management strategies.',
                'priority': 'medium'
            })
    
    # Generate preventive recommendations for low-risk patients
    if risk_level == 'Low' and data:
        preventive_recs = generate_preventive_recommendations(data)
        recommendations.extend(preventive_recs)
    
    return recommendations[:8]  # Increased limit to accommodate preventive recommendations

def generate_preventive_recommendations(data):
    """Generate preventive recommendations for low-risk patients to maintain health"""
    preventive_recs = []
    
    # Analyze current values and provide specific preventive advice
    age = float(data.get('age', 0))
    bmi = float(data.get('BMI', 0))
    sys_bp = float(data.get('sysBP', 0))
    dia_bp = float(data.get('diaBP', 0))
    tot_chol = float(data.get('totChol', 0))
    heart_rate = float(data.get('heartRate', 0))
    glucose = float(data.get('glucose', 0))
    cigs_per_day = float(data.get('cigsPerDay', 0))
    
    # Age-based recommendations
    if age > 40:
        preventive_recs.append({
            'title': 'Age-Related Cardiovascular Monitoring',
            'message': f'As you are {age} years old, it\'s important to be more vigilant about cardiovascular health. Consider more frequent health screenings.',
            'priority': 'preventive',
            'details': 'Risk of cardiovascular disease increases with age. Regular monitoring helps catch issues early.'
        })
    
    # BMI recommendations
    if 18.5 <= bmi <= 24.9:
        preventive_recs.append({
            'title': 'Maintain Healthy Weight',
            'message': f'Your BMI of {bmi:.1f} is in the healthy range. Continue your current diet and exercise routine to maintain this healthy weight.',
            'priority': 'maintenance',
            'details': 'Healthy BMI reduces cardiovascular risk significantly.'
        })
    elif bmi > 24.9:
        preventive_recs.append({
            'title': 'Weight Management for Prevention',
            'message': f'Your BMI of {bmi:.1f} is slightly elevated. Consider gentle weight management to prevent future cardiovascular issues.',
            'priority': 'preventive',
            'details': 'Even small weight reductions can significantly improve cardiovascular health.'
        })
    
    # Blood pressure recommendations
    if 90 <= sys_bp <= 120 and 60 <= dia_bp <= 80:
        preventive_recs.append({
            'title': 'Excellent Blood Pressure Control',
            'message': f'Your blood pressure ({sys_bp:.0f}/{dia_bp:.0f}) is excellent. Continue your current lifestyle to maintain these healthy levels.',
            'priority': 'maintenance',
            'details': 'Optimal blood pressure significantly reduces heart disease risk.'
        })
    elif sys_bp > 120 or dia_bp > 80:
        preventive_recs.append({
            'title': 'Blood Pressure Prevention Strategy',
            'message': f'Your blood pressure ({sys_bp:.0f}/{dia_bp:.0f}) is in the pre-hypertensive range. Focus on prevention through diet, exercise, and stress management.',
            'priority': 'preventive',
            'details': 'Early intervention can prevent progression to hypertension.'
        })
    
    # Cholesterol recommendations
    if tot_chol < 200:
        preventive_recs.append({
            'title': 'Healthy Cholesterol Levels',
            'message': f'Your total cholesterol of {tot_chol:.0f} mg/dL is excellent. Continue heart-healthy eating to maintain these levels.',
            'priority': 'maintenance',
            'details': 'Low cholesterol levels are protective against heart disease.'
        })
    elif 200 <= tot_chol <= 239:
        preventive_recs.append({
            'title': 'Cholesterol Prevention Plan',
            'message': f'Your total cholesterol of {tot_chol:.0f} mg/dL is borderline high. Focus on dietary improvements and regular exercise to prevent further increases.',
            'priority': 'preventive',
            'details': 'Dietary changes and exercise can naturally lower cholesterol levels.'
        })
    
    # Heart rate recommendations
    if 60 <= heart_rate <= 100:
        preventive_recs.append({
            'title': 'Healthy Heart Rate',
            'message': f'Your resting heart rate of {heart_rate:.0f} bpm is normal. Regular cardiovascular exercise can help maintain or improve this.',
            'priority': 'maintenance',
            'details': 'A healthy resting heart rate indicates good cardiovascular fitness.'
        })
    
    # Glucose recommendations
    if 70 <= glucose <= 100:
        preventive_recs.append({
            'title': 'Excellent Blood Sugar Control',
            'message': f'Your blood glucose of {glucose:.0f} mg/dL is in the healthy range. Continue balanced eating to maintain this.',
            'priority': 'maintenance',
            'details': 'Stable blood sugar levels prevent diabetes and reduce cardiovascular risk.'
        })
    
    # Smoking prevention
    if cigs_per_day == 0:
        preventive_recs.append({
            'title': 'Stay Smoke-Free',
            'message': 'Excellent! You don\'t smoke, which significantly reduces your cardiovascular risk. Avoid secondhand smoke exposure.',
            'priority': 'maintenance',
            'details': 'Non-smokers have 50% lower risk of heart disease compared to smokers.'
        })
    
    # General preventive recommendations
    preventive_recs.extend([
        {
            'title': 'Regular Physical Activity',
            'message': 'Aim for at least 150 minutes of moderate-intensity exercise per week to maintain cardiovascular health.',
            'priority': 'preventive',
            'details': 'Regular exercise strengthens the heart muscle and improves circulation.'
        },
        {
            'title': 'Heart-Healthy Diet',
            'message': 'Focus on fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods and sodium.',
            'priority': 'preventive',
            'details': 'A Mediterranean-style diet has been proven to reduce cardiovascular risk.'
        },
        {
            'title': 'Stress Management',
            'message': 'Practice stress-reduction techniques like meditation, yoga, or deep breathing to protect your heart health.',
            'priority': 'preventive',
            'details': 'Chronic stress can contribute to high blood pressure and heart disease.'
        },
        {
            'title': 'Quality Sleep',
            'message': 'Aim for 7-9 hours of quality sleep per night to support overall cardiovascular health.',
            'priority': 'preventive',
            'details': 'Poor sleep quality is associated with increased cardiovascular risk.'
        }
    ])
    
    return preventive_recs[:6]  # Return top 6 preventive recommendations

def analyze_risk_progression(data):
    """Analyze which features could increase risk for low-risk patients"""
    risk_progression_analysis = []
    
    # Define normal ranges and risk thresholds
    normal_ranges = {
        'age': (18, 65),
        'totChol': (0, 200),
        'sysBP': (90, 140),
        'diaBP': (60, 90),
        'BMI': (18.5, 24.9),
        'heartRate': (60, 100),
        'glucose': (70, 100)
    }
    
    # Risk increase thresholds (values that would significantly increase risk)
    risk_thresholds = {
        'totChol': 240,
        'sysBP': 160,
        'diaBP': 100,
        'BMI': 30,
        'heartRate': 120,
        'glucose': 126
    }
    
    current_values = {}
    for feature in normal_ranges.keys():
        if feature in data:
            current_values[feature] = float(data[feature])
    
    # Analyze each feature for risk progression potential
    for feature, current_value in current_values.items():
        normal_min, normal_max = normal_ranges[feature]
        risk_threshold = risk_thresholds.get(feature, normal_max * 1.5)
        
        # Calculate how much increase would be concerning
        if current_value < normal_max:
            increase_to_risk = risk_threshold - current_value
            increase_percentage = (increase_to_risk / current_value) * 100 if current_value > 0 else 0
            
            risk_progression_analysis.append({
                'feature': feature,
                'current_value': current_value,
                'normal_range': f"{normal_min}-{normal_max}",
                'risk_threshold': risk_threshold,
                'increase_to_risk': increase_to_risk,
                'increase_percentage': increase_percentage,
                'vulnerability': 'low' if increase_percentage > 50 else 'medium' if increase_percentage > 25 else 'high',
                'recommendation': generate_feature_specific_prevention(feature, current_value, normal_max, risk_threshold)
            })
    
    return risk_progression_analysis

def generate_feature_specific_prevention(feature, current_value, normal_max, risk_threshold):
    """Generate specific prevention advice for each feature"""
    prevention_advice = {
        'totChol': {
            'diet': 'Focus on soluble fiber (oats, beans, fruits), omega-3 fatty acids (fish, nuts), and limit saturated fats',
            'lifestyle': 'Regular aerobic exercise can help lower cholesterol naturally',
            'monitoring': 'Check cholesterol levels annually or as recommended by your doctor'
        },
        'sysBP': {
            'diet': 'Reduce sodium intake to less than 2,300mg daily, increase potassium-rich foods (bananas, spinach)',
            'lifestyle': 'Regular exercise, stress management, and maintaining healthy weight',
            'monitoring': 'Monitor blood pressure monthly at home and during doctor visits'
        },
        'diaBP': {
            'diet': 'DASH diet (Dietary Approaches to Stop Hypertension) with low sodium',
            'lifestyle': 'Aerobic exercise, meditation, and adequate sleep',
            'monitoring': 'Track diastolic pressure trends over time'
        },
        'BMI': {
            'diet': 'Balanced diet with portion control and mindful eating',
            'lifestyle': '150+ minutes of moderate exercise weekly, strength training 2x/week',
            'monitoring': 'Weigh yourself weekly and track trends'
        },
        'heartRate': {
            'diet': 'Limit caffeine and stimulants that can increase heart rate',
            'lifestyle': 'Regular cardiovascular exercise to strengthen heart muscle',
            'monitoring': 'Monitor resting heart rate trends, especially during stress'
        },
        'glucose': {
            'diet': 'Low glycemic index foods, complex carbohydrates, regular meal timing',
            'lifestyle': 'Regular exercise improves insulin sensitivity',
            'monitoring': 'Annual glucose testing, more frequent if family history of diabetes'
        }
    }
    
    return prevention_advice.get(feature, {
        'diet': 'Maintain balanced nutrition',
        'lifestyle': 'Stay physically active',
        'monitoring': 'Regular health checkups'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'message': 'CHD Prediction API is running'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get input data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Preprocess input
        processed_data = preprocess_input(data)
        if processed_data is None:
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        probabilities = model.predict_proba(processed_data)[0]
        
        # Analyze risk factors
        risk_factors = analyze_risk_factors(data)
        
        # Determine risk level
        chd_probability = probabilities[1]  # Probability of CHD
        if chd_probability < 0.3:
            risk_level = 'Low'
        elif chd_probability < 0.7:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        # Generate recommendations
        recommendations = generate_recommendations(risk_factors, risk_level, data)
        
        # Analyze risk progression for low-risk patients
        risk_progression = None
        if risk_level == 'Low':
            risk_progression = analyze_risk_progression(data)
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'risk_level': risk_level,
            'probability': {
                'chd': float(chd_probability),
                'no_chd': float(probabilities[0])
            },
            'risk_analysis': {
                'total_risk_factors': len(risk_factors),
                'risk_factors': risk_factors
            },
            'recommendations': recommendations,
            'risk_progression': risk_progression,  # Only included for low-risk patients
            'visualization': True  # Indicate that visualization is available
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """Risk analysis endpoint"""
    try:
        # Get input data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Analyze risk factors
        risk_factors = analyze_risk_factors(data)
        normal_values = []
        
        # Check for normal values
        normal_ranges = {
            'age': (18, 65),
            'totChol': (0, 200),
            'sysBP': (90, 140),
            'diaBP': (60, 90),
            'BMI': (18.5, 24.9),
            'heartRate': (60, 100),
            'glucose': (70, 100)
        }
        
        for feature, (min_val, max_val) in normal_ranges.items():
            if feature in data:
                value = float(data[feature])
                if min_val <= value <= max_val:
                    normal_values.append({
                        'feature': feature,
                        'value': value,
                        'status': 'Normal'
                    })
        
        response = {
            'total_risk_factors': len(risk_factors),
            'total_normal_values': len(normal_values),
            'risk_factors': risk_factors,
            'normal_values': normal_values,
            'visualization': True
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'CHD Prediction API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'predict': '/predict',
            'analyze': '/analyze'
        }
    })

if __name__ == '__main__':
    try:
        # Load model on startup
        print("Loading model...")
        if not load_model():
            print("Failed to load model. Please ensure model files exist.")
            exit(1)
        print("Model loaded successfully!")
        
        # Get configuration
        config_name = os.environ.get('FLASK_ENV', 'development')
        try:
            app.config.from_object(config[config_name])
        except:
            # Use simple configuration if config fails
            app.config['API_HOST'] = '0.0.0.0'
            app.config['API_PORT'] = 5000
            app.config['DEBUG'] = True
        
        # Start the server
        print("Starting CHD Prediction API server...")
        print(f"Server will run on {app.config['API_HOST']}:{app.config['API_PORT']}")
        app.run(
            host=app.config['API_HOST'],
            port=app.config['API_PORT'],
            debug=app.config['DEBUG']
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()




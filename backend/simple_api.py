#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple CHD Prediction API
Flask API for Cardiovascular Disease Risk Prediction
"""

import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

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
        
        print("Model loaded successfully")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
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
        print(f"Error preprocessing input: {e}")
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

def generate_recommendations(risk_factors, risk_level):
    """Generate health recommendations based on risk factors"""
    recommendations = []
    
    if risk_level == 'High':
        recommendations.extend([
            {
                'title': 'Immediate Medical Consultation',
                'message': 'Please consult with a healthcare provider immediately for comprehensive cardiovascular assessment.'
            },
            {
                'title': 'Lifestyle Changes',
                'message': 'Focus on diet, exercise, and stress management under medical supervision.'
            }
        ])
    
    # Specific recommendations based on risk factors
    for factor in risk_factors:
        if factor['feature'] == 'smoking':
            recommendations.append({
                'title': 'Quit Smoking',
                'message': 'Smoking significantly increases cardiovascular risk. Consider smoking cessation programs.'
            })
        elif factor['feature'] == 'BMI':
            recommendations.append({
                'title': 'Weight Management',
                'message': 'Maintain a healthy weight through balanced diet and regular exercise.'
            })
        elif factor['feature'] == 'sysBP' or factor['feature'] == 'diaBP':
            recommendations.append({
                'title': 'Blood Pressure Management',
                'message': 'Monitor blood pressure regularly and follow medical advice for hypertension management.'
            })
        elif factor['feature'] == 'totChol':
            recommendations.append({
                'title': 'Cholesterol Management',
                'message': 'Follow a heart-healthy diet and consider cholesterol management strategies.'
            })
    
    return recommendations[:5]  # Limit to 5 recommendations

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
        recommendations = generate_recommendations(risk_factors, risk_level)
        
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
            'visualization': True  # Indicate that visualization is available
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Prediction error: {e}")
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
        print(f"Analysis error: {e}")
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
        
        # Start the server
        print("Starting CHD Prediction API server...")
        print("Server will run on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()


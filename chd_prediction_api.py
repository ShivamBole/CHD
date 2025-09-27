#!/usr/bin/env python3
"""
CHD Prediction API Server
A Flask-based API server for predicting Coronary Heart Disease risk
with feature importance analysis and React frontend integration.
"""

import pandas as pd
import numpy as np
import pickle
import json
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'], 
     methods=['GET', 'POST', 'OPTIONS'], 
     allow_headers=['Content-Type', 'Authorization'])

# Global variables for model and scaler
model = None
scaler = None
feature_names = None
feature_importance = None

# Normal ranges for health metrics (for risk assessment)
NORMAL_RANGES = {
    'age': (18, 65),  # Normal adult range
    'sysBP': (90, 120),  # Normal systolic BP
    'diaBP': (60, 80),   # Normal diastolic BP
    'totChol': (0, 200),  # Normal total cholesterol
    'BMI': (18.5, 24.9),  # Normal BMI range
    'heartRate': (60, 100),  # Normal heart rate
    'glucose': (70, 100),   # Normal glucose level
    'cigsPerDay': (0, 0)    # No smoking is normal
}

def load_model():
    """Load the trained model and scaler"""
    global model, scaler, feature_names, feature_importance
    
    try:
        # Load the trained model
        with open('data/model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Load the scaler
        with open('data/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        # Load feature names
        with open('data/feature_columns.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        
        # Get feature importance from the model
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(zip(feature_names, model.feature_importances_))
        else:
            # For models without feature_importances_, use coefficients
            feature_importance = {name: 0.1 for name in feature_names}
            
        print("Model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def preprocess_input(data):
    """Preprocess input data for prediction"""
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data])
        
        # Handle categorical variables
        df['sex'] = df['sex'].map({'M': 1, 'F': 0})
        df['is_smoking'] = df['is_smoking'].map({'YES': 1, 'NO': 0})
        df['BPMeds'] = df['BPMeds'].map({'YES': 1, 'NO': 0})
        df['prevalentStroke'] = df['prevalentStroke'].map({'YES': 1, 'NO': 0})
        df['prevalentHyp'] = df['prevalentHyp'].map({'YES': 1, 'NO': 0})
        df['diabetes'] = df['diabetes'].map({'YES': 1, 'NO': 0})
        
        # Ensure all required columns are present
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training data
        df = df[feature_names]
        
        # Scale the features
        df_scaled = scaler.transform(df)
        
        return df_scaled
        
    except Exception as e:
        print(f"Error preprocessing data: {e}")
        return None

def analyze_feature_risk(data):
    """Analyze which features are above normal levels"""
    risk_factors = []
    normal_values = []
    abnormal_values = []
    
    for feature, value in data.items():
        if feature in NORMAL_RANGES:
            min_val, max_val = NORMAL_RANGES[feature]
            
            if feature == 'cigsPerDay':
                # For smoking, any value > 0 is abnormal
                if float(value) > 0:
                    risk_factors.append({
                        'feature': feature,
                        'value': value,
                        'normal_range': f"0 (No smoking)",
                        'status': 'High Risk',
                        'message': f"Smoking {value} cigarettes per day significantly increases CHD risk"
                    })
                    abnormal_values.append({
                        'feature': feature,
                        'value': value,
                        'normal_range': f"0 (No smoking)"
                    })
                else:
                    normal_values.append({
                        'feature': feature,
                        'value': value,
                        'normal_range': f"0 (No smoking)"
                    })
            else:
                if float(value) < min_val or float(value) > max_val:
                    risk_factors.append({
                        'feature': feature,
                        'value': value,
                        'normal_range': f"{min_val}-{max_val}",
                        'status': 'High Risk' if float(value) > max_val else 'Low Risk',
                        'message': f"{feature} is {'above' if float(value) > max_val else 'below'} normal range"
                    })
                    abnormal_values.append({
                        'feature': feature,
                        'value': value,
                        'normal_range': f"{min_val}-{max_val}"
                    })
                else:
                    normal_values.append({
                        'feature': feature,
                        'value': value,
                        'normal_range': f"{min_val}-{max_val}"
                    })
    
    return {
        'risk_factors': risk_factors,
        'normal_values': normal_values,
        'abnormal_values': abnormal_values,
        'total_risk_factors': len(risk_factors)
    }

def create_risk_visualization(data, risk_analysis):
    """Create visualization of risk factors"""
    try:
        # Create a figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('CHD Risk Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Feature Importance
        if feature_importance:
            features = list(feature_importance.keys())
            importance = list(feature_importance.values())
            
            # Sort by importance
            sorted_data = sorted(zip(features, importance), key=lambda x: x[1], reverse=True)
            top_features = sorted_data[:10]  # Top 10 features
            
            ax1.barh([f[0] for f in top_features], [f[1] for f in top_features])
            ax1.set_title('Top 10 Feature Importance')
            ax1.set_xlabel('Importance Score')
        
        # 2. Risk Factors Count
        risk_count = len(risk_analysis['risk_factors'])
        normal_count = len(risk_analysis['normal_values'])
        
        ax2.pie([risk_count, normal_count], 
                labels=['Risk Factors', 'Normal Values'],
                colors=['#ff6b6b', '#51cf66'],
                autopct='%1.1f%%')
        ax2.set_title('Risk vs Normal Factors')
        
        # 3. Blood Pressure Analysis
        bp_data = {
            'Systolic BP': data.get('sysBP', 0),
            'Diastolic BP': data.get('diaBP', 0)
        }
        ax3.bar(bp_data.keys(), bp_data.values(), color=['#ff6b6b', '#ff8e53'])
        ax3.set_title('Blood Pressure Levels')
        ax3.set_ylabel('mmHg')
        
        # Add normal range lines
        ax3.axhline(y=120, color='green', linestyle='--', alpha=0.7, label='Normal Sys BP')
        ax3.axhline(y=80, color='blue', linestyle='--', alpha=0.7, label='Normal Dia BP')
        ax3.legend()
        
        # 4. Cholesterol and BMI
        chol_bmi_data = {
            'Total Cholesterol': data.get('totChol', 0),
            'BMI': data.get('BMI', 0)
        }
        ax4.bar(chol_bmi_data.keys(), chol_bmi_data.values(), color=['#ffd43b', '#69db7c'])
        ax4.set_title('Cholesterol and BMI')
        ax4.set_ylabel('Value')
        
        # Add normal range lines
        ax4.axhline(y=200, color='green', linestyle='--', alpha=0.7, label='Normal Cholesterol')
        ax4.axhline(y=24.9, color='blue', linestyle='--', alpha=0.7, label='Normal BMI')
        ax4.legend()
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return plot_data
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return None

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'message': 'CHD Prediction API Server',
        'version': '1.0.0',
        'endpoints': {
            '/predict': 'POST - Predict CHD risk',
            '/analyze': 'POST - Analyze risk factors',
            '/health': 'GET - API health check'
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': pd.Timestamp.now().isoformat(),
        'cors_enabled': True
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'CHD Prediction API is running',
        'version': '1.0.0',
        'endpoints': ['/health', '/predict', '/analyze']
    })

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """Predict CHD risk for given patient data"""
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
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
        prediction_proba = model.predict_proba(processed_data)[0]
        
        # Get risk analysis
        risk_analysis = analyze_feature_risk(data)
        
        # Create visualization
        visualization = create_risk_visualization(data, risk_analysis)
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'risk_level': 'High Risk' if prediction == 1 else 'Low Risk',
            'probability': {
                'no_chd': float(prediction_proba[0]),
                'chd': float(prediction_proba[1])
            },
            'risk_analysis': risk_analysis,
            'feature_importance': feature_importance,
            'visualization': visualization,
            'recommendations': generate_recommendations(risk_analysis, prediction)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze risk factors without prediction"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get risk analysis
        risk_analysis = analyze_feature_risk(data)
        
        # Create visualization
        visualization = create_risk_visualization(data, risk_analysis)
        
        response = {
            'risk_analysis': risk_analysis,
            'feature_importance': feature_importance,
            'visualization': visualization,
            'recommendations': generate_recommendations(risk_analysis, None)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_recommendations(risk_analysis, prediction):
    """Generate health recommendations based on risk analysis"""
    recommendations = []
    
    # General recommendations
    if risk_analysis['total_risk_factors'] > 3:
        recommendations.append({
            'type': 'urgent',
            'title': 'High Risk Detected',
            'message': 'Multiple risk factors detected. Please consult with a healthcare professional immediately.'
        })
    
    # Specific recommendations based on risk factors
    for risk_factor in risk_analysis['risk_factors']:
        feature = risk_factor['feature']
        
        if feature == 'sysBP' and risk_factor['value'] > 140:
            recommendations.append({
                'type': 'warning',
                'title': 'High Blood Pressure',
                'message': 'Your systolic blood pressure is elevated. Consider lifestyle changes and consult a doctor.'
            })
        elif feature == 'totChol' and risk_factor['value'] > 240:
            recommendations.append({
                'type': 'warning',
                'title': 'High Cholesterol',
                'message': 'Your cholesterol levels are high. Consider dietary changes and regular exercise.'
            })
        elif feature == 'BMI' and risk_factor['value'] > 30:
            recommendations.append({
                'type': 'warning',
                'title': 'Obesity Risk',
                'message': 'Your BMI indicates obesity. Weight management and exercise are recommended.'
            })
        elif feature == 'cigsPerDay' and risk_factor['value'] > 0:
            recommendations.append({
                'type': 'critical',
                'title': 'Smoking Cessation',
                'message': 'Smoking significantly increases CHD risk. Consider smoking cessation programs.'
            })
    
    # General health recommendations
    recommendations.extend([
        {
            'type': 'info',
            'title': 'Regular Exercise',
            'message': 'Aim for at least 150 minutes of moderate exercise per week.'
        },
        {
            'type': 'info',
            'title': 'Healthy Diet',
            'message': 'Focus on fruits, vegetables, whole grains, and lean proteins.'
        },
        {
            'type': 'info',
            'title': 'Regular Checkups',
            'message': 'Schedule regular health checkups with your healthcare provider.'
        }
    ])
    
    return recommendations

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        print("Starting CHD Prediction API Server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load model. Please check model.pkl file.")
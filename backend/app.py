"""
FastAPI Application for CHD Prediction
Provides REST API endpoints for making predictions
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import pickle
import pandas as pd
import numpy as np
import os
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger("chd_prediction")

# Define normal ranges for health metrics
NORMAL_RANGES = {
    "age": {"min": 20, "max": 120, "unit": "years"},
    "education": {"description": "Education level (categorical)"},
    "sex": {"description": "Gender (categorical)"},
    "is_smoking": {"description": "Smoking status (categorical)"},
    "cigsPerDay": {"min": 0, "max": 0, "ideal": 0, "unit": "cigarettes"},
    "BPMeds": {"min": 0, "max": 0, "ideal": 0, "unit": "medication"},
    "prevalentStroke": {"min": 0, "max": 0, "ideal": 0, "unit": "boolean"},
    "prevalentHyp": {"min": 0, "max": 0, "ideal": 0, "unit": "boolean"},
    "diabetes": {"min": 0, "max": 0, "ideal": 0, "unit": "boolean"},
    "totChol": {"min": 125, "max": 200, "unit": "mg/dL"},
    "sysBP": {"min": 90, "max": 120, "unit": "mmHg"},
    "diaBP": {"min": 60, "max": 80, "unit": "mmHg"},
    "BMI": {"min": 18.5, "max": 24.9, "unit": "kg/m²"},
    "heartRate": {"min": 60, "max": 100, "unit": "bpm"},
    "glucose": {"min": 70, "max": 100, "unit": "mg/dL"}
}

# Global variables for model and scaler
model = None
scaler = None
model_info = None

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

def generate_preventive_recommendations(data):
    """Generate preventive recommendations based on user data"""
    preventive_recs = []
    
    # Check for features that are close to risk thresholds
    features_to_monitor = []
    
    # Check each feature against normal ranges
    for feature, value in data.items():
        if feature in NORMAL_RANGES and "max" in NORMAL_RANGES[feature]:
            normal_max = NORMAL_RANGES[feature]["max"]
            # If value is within 15% of max normal range, flag it for monitoring
            if isinstance(value, (int, float)) and value > normal_max * 0.85 and value <= normal_max:
                features_to_monitor.append({
                    'feature': feature,
                    'current': value,
                    'normal_max': normal_max
                })
    
    # Generate recommendations for features to monitor
    for feature_data in features_to_monitor:
        feature = feature_data['feature']
        current = feature_data['current']
        normal_max = feature_data['normal_max']
        
        # Get feature-specific advice
        advice = generate_feature_specific_prevention(
            feature, 
            current, 
            normal_max, 
            normal_max * 1.1  # 10% above normal as risk threshold
        )
        
        preventive_recs.append({
            'title': f'Monitor Your {feature}',
            'message': f'Your {feature} is within normal range but approaching upper limits. {advice["diet"]}',
            'priority': 'preventive',
            'advice': advice
        })
    
    return preventive_recs

def generate_recommendations(risk_factors, risk_level, data=None):
    """Generate health recommendations based on risk factors and current health status"""
    recommendations = []
    
    if risk_level == 'HIGH RISK':
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
    
    elif risk_level == 'MEDIUM RISK':
        recommendations.extend([
            {
                'title': 'Schedule Medical Consultation',
                'message': 'Schedule an appointment with your healthcare provider within the next month for cardiovascular assessment.',
                'priority': 'medium'
            },
            {
                'title': 'Lifestyle Modifications',
                'message': 'Begin implementing heart-healthy diet changes and regular exercise routine.',
                'priority': 'medium'
            },
            {
                'title': 'Monitor Health Metrics',
                'message': 'Regularly monitor your blood pressure, cholesterol, and other key health indicators.',
                'priority': 'medium'
            }
        ])
 
    elif risk_level == 'LOW RISK':
        # Preventive recommendations for low-risk patients
        recommendations.extend([
            {
                'title': 'Maintain Current Health Status',
                'message': 'Congratulations! Your current health profile shows low risk for heart disease. Continue maintaining your healthy lifestyle.',
                'priority': 'maintenance'
            }
        ])
    
    # Specific recommendations based on risk factors
    for factor in risk_factors:
        if factor['feature'] == 'is_smoking' and factor['status'] == 'High':
            recommendations.append({
                'title': 'Quit Smoking',
                'message': 'Smoking significantly increases cardiovascular risk. Consider smoking cessation programs.',
                'priority': 'high'
            })
        elif factor['feature'] == 'BMI' and factor['status'] == 'High':
            recommendations.append({
                'title': 'Weight Management',
                'message': 'Maintain a healthy weight through balanced diet and regular exercise.',
                'priority': 'medium'
            })
        elif (factor['feature'] == 'sysBP' or factor['feature'] == 'diaBP') and factor['status'] == 'High':
            recommendations.append({
                'title': 'Blood Pressure Management',
                'message': 'Monitor blood pressure regularly and follow medical advice for hypertension management.',
                'priority': 'high'
            })
        elif factor['feature'] == 'totChol' and factor['status'] == 'High':
            recommendations.append({
                'title': 'Cholesterol Management',
                'message': 'Follow a heart-healthy diet and consider cholesterol management strategies.',
                'priority': 'medium'
            })
        elif factor['feature'] == 'glucose' and factor['status'] == 'High':
            recommendations.append({
                'title': 'Blood Sugar Management',
                'message': 'Monitor blood glucose levels and consider dietary changes to manage blood sugar.',
                'priority': 'medium'
            })
    
    # Generate preventive recommendations for low-risk patients
    if risk_level == 'Low' and data:
        preventive_recs = generate_preventive_recommendations(data)
        recommendations.extend(preventive_recs)
    
    return recommendations[:8]  # Limit to 8 recommendations

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup"""
    logger.info("Loading model on startup...")
    load_model()
    yield
    logger.info("Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="CHD Prediction API",
    description="API for predicting 10-year risk of Coronary Heart Disease",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log request information and timing"""
    start_time = time.time()
    
    # Get request details
    method = request.method
    url = request.url.path
    
    # Process the request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log request details
        logger.info(f"{method} {url} completed in {process_time:.4f}s - Status: {response.status_code}")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"{method} {url} failed after {process_time:.4f}s - Error: {str(e)}")
        raise

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Categorical mappings for frontend
CATEGORICAL_MAPPINGS = {
    'sex': {'M': 1, 'F': 0, 'Male': 1, 'Female': 0},
    'is_smoking': {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0},
    'BPMeds': {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0},
    'prevalentStroke': {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0},
    'prevalentHyp': {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0},
    'diabetes': {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0}
}


class PredictionRequest(BaseModel):
    """Request model for single prediction - accepts both categorical strings and numeric values"""
    age: int = Field(..., ge=0, le=120, description="Age of the patient")
    education: float = Field(..., description="Education level")
    sex: str = Field(..., description="Sex (M/Male or F/Female)")
    is_smoking: str = Field(..., description="Is smoking (YES/Yes or NO/No)")
    cigsPerDay: float = Field(..., ge=0, description="Cigarettes per day")
    BPMeds: str = Field(..., description="Blood pressure medication (YES/Yes or NO/No)")
    prevalentStroke: str = Field(..., description="Prevalent stroke (YES/Yes or NO/No)")
    prevalentHyp: str = Field(..., description="Prevalent hypertension (YES/Yes or NO/No)")
    diabetes: str = Field(..., description="Diabetes (YES/Yes or NO/No)")
    totChol: float = Field(..., ge=0, description="Total cholesterol")
    sysBP: float = Field(..., ge=0, description="Systolic blood pressure")
    diaBP: float = Field(..., ge=0, description="Diastolic blood pressure")
    BMI: float = Field(..., ge=0, description="Body Mass Index")
    heartRate: float = Field(..., ge=0, description="Heart rate")
    glucose: float = Field(..., ge=0, description="Glucose level")


class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions"""
    patients: List[PredictionRequest]


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    prediction: int = Field(..., description="Prediction (0=Low Risk, 1=High Risk)")
    risk_level: str = Field(..., description="Risk level description")
    probability_no_disease: float = Field(..., description="Probability of no disease")
    probability_disease: float = Field(..., description="Probability of disease")
    confidence: float = Field(..., description="Confidence score")
    model_name: str = Field(..., description="Model used for prediction")
    risk_factors: List[Dict[str, Any]] = Field(default=[], description="Risk factors contributing to prediction")
    recommendations: List[Dict[str, Any]] = Field(default=[], description="Health recommendations based on risk factors")
    normal_ranges: Dict[str, Any] = Field(default={}, description="Normal ranges for health metrics")
    actual_values: Dict[str, Any] = Field(default={}, description="Actual values for health metrics")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_name: Optional[str] = None
    timestamp: str


def map_categorical_to_numeric(value: str, field: str) -> int:
    """
    Map categorical string values to numeric values
    
    Args:
        value: Categorical value (e.g., 'M', 'F', 'YES', 'NO')
        field: Field name (e.g., 'sex', 'is_smoking')
        
    Returns:
        Numeric value (0 or 1)
    """
    if field in CATEGORICAL_MAPPINGS:
        mapping = CATEGORICAL_MAPPINGS[field]
        # Try to find the value in mapping (case insensitive)
        for key, num_value in mapping.items():
            if value.upper() == key.upper():
                return num_value
        raise ValueError(f"Invalid value '{value}' for field '{field}'. Valid values: {list(mapping.keys())}")
    return value


def load_model():
    """Load the best model and scaler with caching and improved error handling"""
    global model, scaler, model_info
    
    # Check if model is already loaded
    if model is not None and scaler is not None and model_info is not None:
        logger.info("Model already loaded, using cached version")
        return True
    
    try:
        import json
        import os
        
        # Check if model files exist
        model_path = 'models/best_model.pkl'
        scaler_path = 'models/scaler.pkl'
        info_path = 'models/best_model_info.json'
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at {model_path}")
            return False
            
        if not os.path.exists(scaler_path):
            logger.error(f"Scaler file not found at {scaler_path}")
            return False
            
        if not os.path.exists(info_path):
            logger.error(f"Model info file not found at {info_path}")
            return False
        
        # Load model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Load scaler
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        # Load model info
        with open(info_path, 'r') as f:
            model_info = json.load(f)
        
        logger.info(f"Model '{model_info.get('model_name')}' and scaler loaded successfully")
        return True
    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        return False
    except pickle.UnpicklingError as e:
        logger.error(f"Error unpickling model or scaler: {str(e)}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing model info JSON: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error loading model: {str(e)}")
        return False


@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "message": "CHD Prediction API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "model_name": model_info.get('model_name') if model_info else None,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Predict CHD risk for a single patient
    
    Returns prediction with confidence, probabilities, risk factors, and recommendations
    """
    # Check if model is loaded
    if model is None or scaler is None:
        # Try to load the model if not already loaded
        if not load_model():
            raise HTTPException(status_code=503, detail="Model not loaded and could not be loaded automatically")
    
    try:
        # Map categorical values to numeric
        try:
            sex_numeric = map_categorical_to_numeric(request.sex, 'sex')
            is_smoking_numeric = map_categorical_to_numeric(request.is_smoking, 'is_smoking')
            BPMeds_numeric = map_categorical_to_numeric(request.BPMeds, 'BPMeds')
            prevalentStroke_numeric = map_categorical_to_numeric(request.prevalentStroke, 'prevalentStroke')
            prevalentHyp_numeric = map_categorical_to_numeric(request.prevalentHyp, 'prevalentHyp')
            diabetes_numeric = map_categorical_to_numeric(request.diabetes, 'diabetes')
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Create data dictionary for risk factor analysis
        data_dict = {
            'age': request.age,
            'education': request.education,
            'sex': sex_numeric,
            'is_smoking': is_smoking_numeric,
            'cigsPerDay': request.cigsPerDay,
            'BPMeds': BPMeds_numeric,
            'prevalentStroke': prevalentStroke_numeric,
            'prevalentHyp': prevalentHyp_numeric,
            'diabetes': diabetes_numeric,
            'totChol': request.totChol,
            'sysBP': request.sysBP,
            'diaBP': request.diaBP,
            'BMI': request.BMI,
            'heartRate': request.heartRate,
            'glucose': request.glucose
        }
        
        # Convert request to DataFrame with correct column order
        data = pd.DataFrame({
            'age': [request.age],
            'education': [request.education],
            'sex': [sex_numeric],
            'is_smoking': [is_smoking_numeric],
            'cigsPerDay': [request.cigsPerDay],
            'BPMeds': [BPMeds_numeric],
            'prevalentStroke': [prevalentStroke_numeric],
            'prevalentHyp': [prevalentHyp_numeric],
            'diabetes': [diabetes_numeric],
            'totChol': [request.totChol],
            'sysBP': [request.sysBP],
            'diaBP': [request.diaBP],
            'BMI': [request.BMI],
            'heartRate': [request.heartRate],
            'glucose': [request.glucose]
        })
        
        # Ensure all values are numeric
        for col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Scale the data
        data_scaled = scaler.transform(data)
        
        # Make prediction
        prediction = model.predict(data_scaled)[0]
        probabilities = model.predict_proba(data_scaled)[0]
        
        # Determine risk level based on probability of disease
        disease_prob = float(probabilities[1])
        if disease_prob >= 0.4:
            risk_level = "HIGH RISK"
        elif disease_prob >= 0.2:
            risk_level = "MEDIUM RISK"
        else:
            risk_level = "LOW RISK"
        
        # Identify risk factors
        risk_factors = []
        actual_values = {}
        
        # Check each feature against normal ranges
        for feature, value in data_dict.items():
            # Store actual values for frontend display
            if feature in ['sex', 'is_smoking', 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes']:
                # For categorical features, store the original string value
                field_value = getattr(request, feature)
                actual_values[feature] = field_value
            else:
                # For numerical features, store the numeric value
                actual_values[feature] = value
                
            # Check if feature is outside normal range
            if feature in NORMAL_RANGES and "max" in NORMAL_RANGES[feature]:
                normal_max = NORMAL_RANGES[feature]["max"]
                if isinstance(value, (int, float)) and value > normal_max:
                    risk_factors.append({
                        'feature': feature,
                        'value': value,
                        'normal_max': normal_max,
                        'status': 'High'
                    })
            
            # Special handling for categorical risk factors
            if feature == 'is_smoking' and value == 1:
                risk_factors.append({
                    'feature': feature,
                    'value': value,
                    'status': 'High'
                })
            
            if feature == 'prevalentHyp' and value == 1:
                risk_factors.append({
                    'feature': feature,
                    'value': value,
                    'status': 'High'
                })
                
            if feature == 'diabetes' and value == 1:
                risk_factors.append({
                    'feature': feature,
                    'value': value,
                    'status': 'High'
                })
        
        # Generate recommendations based on risk factors and risk level
        recommendations = generate_recommendations(risk_factors, risk_level, data_dict)
        
        # Prepare response
        response = {
            "prediction": int(prediction),
            "risk_level": risk_level,
            "probability_no_disease": float(probabilities[0]),
            "probability_disease": float(probabilities[1]),
            "confidence": float(max(probabilities)),
            "model_name": model_info.get('model_name', 'Unknown') if model_info else 'Unknown',
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "normal_ranges": NORMAL_RANGES,
            "actual_values": actual_values
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/model/info", tags=["Model"])
async def get_model_info():
    """Get information about the loaded model"""
    if model_info is None:
        raise HTTPException(status_code=503, detail="Model info not available")
    
    return {
        "model_name": model_info.get('model_name'),
        "metrics": model_info.get('metrics', {}),
        "loaded_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CHD Prediction API...")
    logger.info("API Documentation available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)


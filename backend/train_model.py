#!/usr/bin/env python3
"""
CHD Model Training Script
Trains a Random Forest model for CHD prediction and saves it for API use.
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    """Load and preprocess the cardiovascular dataset"""
    try:
        # Load the dataset
        df = pd.read_csv("../data/raw/data_cardiovascular_risk.csv")
        print(f"Dataset loaded: {df.shape}")
        
        # Handle missing values
        df.dropna(axis=0, inplace=True)
        print(f"After dropping missing values: {df.shape}")
        
        # Encode categorical variables
        categorical_features = ['sex', 'education', 'is_smoking', 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes']
        
        for feature in categorical_features:
            if feature in df.columns:
                le = LabelEncoder()
                df[feature] = le.fit_transform(df[feature])
        
        # Define feature columns
        feature_columns = [
            'age', 'education', 'sex', 'is_smoking', 'cigsPerDay',
            'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes',
            'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose'
        ]
        
        # Prepare features and target
        X = df[feature_columns]
        y = df['TenYearCHD']
        
        print(f"Features shape: {X.shape}")
        print(f"Target distribution: {y.value_counts()}")
        
        return X, y, feature_columns
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None

def train_model(X, y, feature_columns):
    """Train the Random Forest model"""
    try:
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Initialize scaler
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Define parameter grid for Random Forest
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],
            'max_features': ['sqrt', 'log2']
        }
        
        # Initialize Random Forest
        rf_classifier = RandomForestClassifier(random_state=42)
        
        # Adjust CV based on dataset size
        cv_folds = min(5, len(X_train) // 2) if len(X_train) > 4 else 2
        
        # Grid Search
        print(f"Starting grid search with {cv_folds} CV folds...")
        grid_search = GridSearchCV(
            rf_classifier, 
            param_grid, 
            cv=cv_folds, 
            n_jobs=-1,
            scoring='accuracy'
        )
        
        # Train the model
        grid_search.fit(X_train_scaled, y_train)
        
        # Get best parameters
        best_params = grid_search.best_params_
        print(f"Best parameters: {best_params}")
        
        # Make predictions
        y_pred = grid_search.predict(X_test_scaled)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
        
        # Print classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save the model and scaler
        with open('data/model.pkl', 'wb') as f:
            pickle.dump(grid_search, f)
        
        with open('data/scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        
        # Save feature columns
        with open('data/feature_columns.pkl', 'wb') as f:
            pickle.dump(feature_columns, f)
        
        print("Model saved successfully!")
        
        return grid_search, scaler, feature_columns
        
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None, None

def main():
    """Main training function"""
    print("Starting CHD Model Training...")
    
    # Load and preprocess data
    X, y, feature_columns = load_and_preprocess_data()
    
    if X is None:
        print("Failed to load data. Exiting.")
        return
    
    # Train the model
    model, scaler, features = train_model(X, y, feature_columns)
    
    if model is None:
        print("Failed to train model. Exiting.")
        return
    
    print("Training completed successfully!")
    print("Files created:")
    print("- data/model.pkl (trained model)")
    print("- data/scaler.pkl (feature scaler)")
    print("- data/feature_columns.pkl (feature names)")

if __name__ == "__main__":
    main()
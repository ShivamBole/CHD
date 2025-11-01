"""
Data Preprocessing Pipeline for CHD Prediction
Handles data loading, cleaning, feature engineering, and transformation
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import pickle
import os


class DataPreprocessor:
    """Class to handle all data preprocessing operations"""
    
    def __init__(self, data_path, random_state=42):
        """
        Initialize the DataPreprocessor
        
        Args:
            data_path: Path to the CSV data file
            random_state: Random state for reproducibility
        """
        self.data_path = data_path
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.smote = SMOTE(random_state=random_state)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self):
        """Load data from CSV file"""
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Data loaded successfully. Shape: {self.df.shape}")
        return self.df
    
    def handle_missing_values(self):
        """Handle missing values in the dataset"""
        print("Handling missing values...")
        # Drop ID column if exists
        if 'id' in self.df.columns:
            self.df = self.df.drop('id', axis=1)
        
        # Fill missing values with median for numeric columns
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna(self.df[col].median(), inplace=True)
        
        # Fill missing values with mode for categorical columns
        categorical_columns = self.df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        
        print("Missing values handled successfully")
        return self.df
    
    def encode_categorical_features(self):
        """Encode categorical features to numeric"""
        print("Encoding categorical features...")
        
        # Define categorical features
        categorical_features = ['sex', 'education', 'is_smoking', 'BPMeds', 
                              'prevalentStroke', 'prevalentHyp', 'diabetes']
        
        # Label encoding for binary categorical features
        if 'sex' in self.df.columns:
            self.df['sex'] = self.df['sex'].map({'F': 0, 'M': 1})
        
        if 'is_smoking' in self.df.columns:
            self.df['is_smoking'] = self.df['is_smoking'].map({'NO': 0, 'YES': 1})
        
        # Convert other categorical features to numeric if needed
        for col in categorical_features:
            if col in self.df.columns and self.df[col].dtype == 'object':
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        print("Categorical features encoded successfully")
        return self.df
    
    def split_features_target(self):
        """Split features and target variable"""
        print("Splitting features and target...")
        
        # Separate features and target
        self.X = self.df.drop('TenYearCHD', axis=1)
        self.y = self.df['TenYearCHD']
        
        print(f"Features shape: {self.X.shape}")
        print(f"Target distribution:\n{self.y.value_counts()}")
        
        return self.X, self.y
    
    def apply_smote(self, X, y):
        """Apply SMOTE to balance the dataset"""
        print("Applying SMOTE to balance the dataset...")
        print(f"Before SMOTE - Class distribution:\n{y.value_counts()}")
        
        X_resampled, y_resampled = self.smote.fit_resample(X, y)
        
        print(f"After SMOTE - Class distribution:\n{pd.Series(y_resampled).value_counts()}")
        print(f"Resampled data shape: {X_resampled.shape}")
        
        return X_resampled, y_resampled
    
    def split_train_test(self, X, y, test_size=0.2):
        """Split data into training and testing sets"""
        print("Splitting data into train and test sets...")
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        print(f"Training set shape: {self.X_train.shape}")
        print(f"Testing set shape: {self.X_test.shape}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def scale_features(self):
        """Scale features using StandardScaler"""
        print("Scaling features...")
        
        # Fit scaler on training data and transform both train and test
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Convert back to DataFrame with original column names
        self.X_train = pd.DataFrame(self.X_train_scaled, columns=self.X.columns)
        self.X_test = pd.DataFrame(self.X_test_scaled, columns=self.X.columns)
        
        print("Features scaled successfully")
        
        return self.X_train, self.X_test
    
    def save_scaler(self, filepath='models/scaler.pkl'):
        """Save the scaler for future use"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to {filepath}")
    
    def get_preprocessed_data(self):
        """Get the preprocessed data"""
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def run_full_pipeline(self, apply_smote=True, save_scaler=True):
        """
        Run the complete preprocessing pipeline
        
        Args:
            apply_smote: Whether to apply SMOTE for balancing
            save_scaler: Whether to save the scaler
        """
        print("="*50)
        print("Starting Data Preprocessing Pipeline")
        print("="*50)
        
        # Load data
        self.load_data()
        
        # Handle missing values
        self.handle_missing_values()
        
        # Encode categorical features
        self.encode_categorical_features()
        
        # Split features and target
        X, y = self.split_features_target()
        
        # Apply SMOTE if requested
        if apply_smote:
            X, y = self.apply_smote(X, y)
        
        # Split into train and test
        self.split_train_test(X, y)
        
        # Scale features
        self.scale_features()
        
        # Save scaler if requested
        if save_scaler:
            self.save_scaler()
        
        print("="*50)
        print("Data Preprocessing Pipeline Completed")
        print("="*50)
        
        return self.X_train, self.X_test, self.y_train, self.y_test


if __name__ == "__main__":
    # Example usage
    preprocessor = DataPreprocessor(data_path="data_cardiovascular_risk.csv")
    X_train, X_test, y_train, y_test = preprocessor.run_full_pipeline()
    
    print("\nPreprocessed data ready for model training!")
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")

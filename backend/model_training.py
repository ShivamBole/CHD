"""
Model Training Pipeline for CHD Prediction
Handles model training, hyperparameter tuning, and model saving
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """Class to handle model training and hyperparameter tuning"""
    
    def __init__(self, random_state=42):
        """
        Initialize the ModelTrainer
        
        Args:
            random_state: Random state for reproducibility
        """
        self.random_state = random_state
        self.models = {}
        self.best_models = {}
        self.trained_models = {}
        
    def define_models(self):
        """Define models and their hyperparameter grids"""
        print("Defining models and hyperparameter grids...")
        
        self.models = {
            'LogisticRegression': {
                'model': LogisticRegression(random_state=self.random_state),
                'params': {
                    'penalty': ['l1', 'l2'],
                    'C': [0.01, 0.1, 1, 10, 100],
                    'class_weight': ['balanced', None],
                    'solver': ['liblinear', 'lbfgs']
                }
            },
            'KNeighborsClassifier': {
                'model': KNeighborsClassifier(),
                'params': {
                    'n_neighbors': np.arange(1, 10),
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan']
                }
            },
            'DecisionTreeClassifier': {
                'model': DecisionTreeClassifier(random_state=self.random_state),
                'params': {
                    'max_features': ['auto', 'sqrt', 'log2'],
                    'min_samples_split': [2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'min_samples_leaf': [1, 2, 3, 4, 5],
                    'max_depth': [3, 5, 7, 10, None]
                }
            },
            'RandomForestClassifier': {
                'model': RandomForestClassifier(random_state=self.random_state),
                'params': {
                    'n_estimators': [50, 100, 200],
                    'max_features': ['auto', 'sqrt', 'log2'],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4],
                    'max_depth': [5, 10, 20, None]
                }
            },
            'SVC': {
                'model': SVC(random_state=self.random_state, probability=True),
                'params': {
                    'C': [0.1, 1, 10],
                    'kernel': ['linear', 'rbf', 'poly'],
                    'gamma': ['scale', 'auto']
                }
            }
        }
        
        print(f"Defined {len(self.models)} models")
        return self.models
    
    def train_model(self, model_name, X_train, y_train, cv=5, n_jobs=-1):
        """
        Train a single model with GridSearchCV
        
        Args:
            model_name: Name of the model to train
            X_train: Training features
            y_train: Training target
            cv: Number of cross-validation folds
            n_jobs: Number of parallel jobs
        """
        print(f"\n{'='*50}")
        print(f"Training {model_name}...")
        print(f"{'='*50}")
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found in defined models")
        
        model_config = self.models[model_name]
        model = model_config['model']
        params = model_config['params']
        
        # Perform GridSearchCV
        grid_search = GridSearchCV(
            model, 
            params, 
            cv=cv, 
            scoring='f1',
            n_jobs=n_jobs,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        # Store the best model
        self.best_models[model_name] = grid_search.best_estimator_
        
        print(f"Best parameters for {model_name}:")
        print(grid_search.best_params_)
        print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def train_all_models(self, X_train, y_train, cv=5, n_jobs=-1):
        """
        Train all defined models
        
        Args:
            X_train: Training features
            y_train: Training target
            cv: Number of cross-validation folds
            n_jobs: Number of parallel jobs
        """
        print("\n" + "="*50)
        print("Training All Models")
        print("="*50)
        
        if not self.models:
            self.define_models()
        
        for model_name in self.models.keys():
            try:
                trained_model = self.train_model(model_name, X_train, y_train, cv, n_jobs)
                self.trained_models[model_name] = trained_model
            except Exception as e:
                print(f"Error training {model_name}: {str(e)}")
                continue
        
        print("\n" + "="*50)
        print("All Models Trained Successfully")
        print("="*50)
        
        return self.trained_models
    
    def save_model(self, model, model_name, filepath=None):
        """
        Save a trained model to disk
        
        Args:
            model: Trained model object
            model_name: Name of the model
            filepath: Path to save the model (optional)
        """
        if filepath is None:
            filepath = f'models/{model_name}.pkl'
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Model saved to {filepath}")
    
    def save_all_models(self, base_path='models/'):
        """
        Save all trained models to disk
        
        Args:
            base_path: Base directory to save models
        """
        print("\nSaving all trained models...")
        
        os.makedirs(base_path, exist_ok=True)
        
        for model_name, model in self.trained_models.items():
            filepath = os.path.join(base_path, f'{model_name}.pkl')
            self.save_model(model, model_name, filepath)
        
        print(f"All models saved to {base_path}")
    
    def get_best_model(self, X_test, y_test):
        """
        Get the best performing model based on test set
        
        Args:
            X_test: Test features
            y_test: Test target
        """
        from sklearn.metrics import accuracy_score, f1_score
        
        print("\n" + "="*50)
        print("Evaluating All Models on Test Set")
        print("="*50)
        
        results = {}
        
        for model_name, model in self.trained_models.items():
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            results[model_name] = {
                'accuracy': accuracy,
                'f1_score': f1,
                'model': model
            }
            
            print(f"{model_name}:")
            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  F1 Score: {f1:.4f}")
        
        # Find best model based on F1 score
        best_model_name = max(results, key=lambda x: results[x]['f1_score'])
        best_model = results[best_model_name]['model']
        
        print(f"\nBest Model: {best_model_name}")
        print(f"  Accuracy: {results[best_model_name]['accuracy']:.4f}")
        print(f"  F1 Score: {results[best_model_name]['f1_score']:.4f}")
        
        return best_model_name, best_model, results


if __name__ == "__main__":
    # Example usage
    from data_preprocessing import DataPreprocessor
    
    # Preprocess data
    preprocessor = DataPreprocessor(data_path="data_cardiovascular_risk.csv")
    X_train, X_test, y_train, y_test = preprocessor.run_full_pipeline()
    
    # Train models
    trainer = ModelTrainer()
    trainer.define_models()
    trainer.train_all_models(X_train, y_train)
    
    # Get best model
    best_name, best_model, results = trainer.get_best_model(X_test, y_test)
    
    # Save all models
    trainer.save_all_models()
    
    print("\nModel training completed!")

# """
# Prediction Script using the Best Trained Model
# Loads the best model and makes predictions on new data
# """

# import pickle
# import pandas as pd
# import numpy as np
# import json
# import os
# import warnings
# warnings.filterwarnings('ignore')


# class CHDPredictor:
#     """Class to load and use the best trained model for predictions"""
    
#     def __init__(self, model_path='models/best_model.pkl', scaler_path='models/scaler.pkl'):
#         """
#         Initialize the predictor
        
#         Args: 
#             model_path: Path to the saved best model
#             scaler_path: Path to the saved scaler
#         """
#         self.model_path = model_path
#         self.scaler_path = scaler_path
#         self.model = None
#         self.scaler = None
#         self.model_info = None
        
#     def load_model(self):
#         """Load the best model and scaler"""
#         print("Loading model and scaler...")
        
#         # Load model
#         with open(self.model_path, 'rb') as f:
#             self.model = pickle.load(f)
        
#         # Load scaler
#         with open(self.scaler_path, 'rb') as f:
#             self.scaler = pickle.load(f)
        
#         # Load model info if available
#         info_path = 'models/best_model_info.json'
#         if os.path.exists(info_path):
#             with open(info_path, 'r') as f:
#                 self.model_info = json.load(f)
#             print(f"Model loaded: {self.model_info['model_name']}")
#             print(f"Model metrics:")
#             for metric, value in self.model_info['metrics'].items():
#                 print(f"  {metric}: {value:.4f}")
#         else:
#             print("Model loaded successfully")
        
#         return self.model, self.scaler
    
#     def preprocess_data(self, data):
#         """
#         Preprocess input data
        
#         Args:
#             data: DataFrame or array of input features
            
#         Returns:
#             Preprocessed data
#         """
#         # Convert to DataFrame if numpy array
#         if isinstance(data, np.ndarray):
#             data = pd.DataFrame(data)
        
#         # Ensure correct column order (adjust based on your feature order)
#         expected_columns = ['age', 'education', 'sex', 'is_smoking', 'cigsPerDay', 'BPMeds', 
#                           'prevalentStroke', 'prevalentHyp', 'diabetes', 
#                           'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
        
#         # Reorder columns if needed
#         if isinstance(data, pd.DataFrame):
#             data = data[expected_columns]
        
#         # Scale the data
#         data_scaled = self.scaler.transform(data)
        
#         return data_scaled
    
#     def predict(self, data):
#         """
#         Make predictions on new data
        
#         Args:
#             data: DataFrame or array of input features
            
#         Returns:
#             Predictions (0 or 1)
#         """
#         if self.model is None or self.scaler is None:
#             raise ValueError("Model and scaler must be loaded first. Call load_model()")
        
#         # Preprocess data
#         data_processed = self.preprocess_data(data)
        
#         # Make predictions
#         predictions = self.model.predict(data_processed)
        
#         return predictions
    
#     def predict_proba(self, data):
#         """
#         Get prediction probabilities
        
#         Args:
#             data: DataFrame or array of input features
            
#         Returns:
#             Prediction probabilities
#         """
#         if self.model is None or self.scaler is None:
#             raise ValueError("Model and scaler must be loaded first. Call load_model()")
        
#         # Preprocess data
#         data_processed = self.preprocess_data(data)
        
#         # Get probabilities
#         probabilities = self.model.predict_proba(data_processed)
        
#         return probabilities
    
#     def predict_with_confidence(self, data):
#         """
#         Make predictions with confidence scores and risk levels
        
#         Args:
#             data: DataFrame or array of input features
            
#         Returns:
#             Dictionary with predictions, confidence scores, and risk levels
#         """
#         predictions = self.predict(data)
#         probabilities = self.predict_proba(data)
        
#         results = []
#         for pred, prob in zip(predictions, probabilities):
#             # Calculate risk level based on probability of disease
#             disease_prob = float(prob[1])
            
#             if disease_prob >= 0.4:
#                 risk_level = "HIGH RISK"
#             elif disease_prob >= 0.2:
#                 risk_level = "MEDIUM RISK"
#             else:
#                 risk_level = "LOW RISK"
                
#             results.append({
#                 'prediction': int(pred),
#                 'probability_no_disease': float(prob[0]),
#                 'probability_disease': disease_prob,
#                 'confidence': float(max(prob)),
#                 'risk_level': risk_level
#             })
        
#         return results


# def predict_single_sample(age, education, sex, is_smoking, cigsPerDay, BPMeds, 
#                           prevalentStroke, prevalentHyp, diabetes,
#                           totChol, sysBP, diaBP, BMI, heartRate, glucose):
#     """
#     Predict for a single sample
    
#     Args:
#         All feature values
        
#     Returns:
#         Prediction result
#     """
#     # Create sample data
#     sample_data = pd.DataFrame({
#         'age': [age],
#         'education': [education],
#         'sex': [sex],
#         'is_smoking': [is_smoking],
#         'cigsPerDay': [cigsPerDay],
#         'BPMeds': [BPMeds],
#         'prevalentStroke': [prevalentStroke],
#         'prevalentHyp': [prevalentHyp],
#         'diabetes': [diabetes],
#         'totChol': [totChol],
#         'sysBP': [sysBP],
#         'diaBP': [diaBP],
#         'BMI': [BMI],
#         'heartRate': [heartRate],
#         'glucose': [glucose]
#     })
    
#     # Load model and predict
#     predictor = CHDPredictor()
#     predictor.load_model()
    
#     result = predictor.predict_with_confidence(sample_data)[0]
    
#     return result


# def predict_from_csv(csv_path, output_path='predictions.csv'):
#     """
#     Predict for multiple samples from CSV file
    
#     Args:
#         csv_path: Path to CSV file with features
#         output_path: Path to save predictions
#     """
#     # Load data
#     data = pd.read_csv(csv_path)
    
#     # Load model and predict
#     predictor = CHDPredictor()
#     predictor.load_model()
    
#     # Make predictions
#     predictions = predictor.predict(data)
#     probabilities = predictor.predict_proba(data)
    
#     # Add predictions to dataframe
#     data['prediction'] = predictions
#     data['probability_no_disease'] = probabilities[:, 0]
#     data['probability_disease'] = probabilities[:, 1]
#     data['confidence'] = np.max(probabilities, axis=1)
    
#     # Save results
#     data.to_csv(output_path, index=False)
#     print(f"Predictions saved to {output_path}")
    
#     return data


# if __name__ == "__main__":
#     print("="*70)
#     print("CHD Prediction - Load Best Model")
#     print("="*70)
    
#     # Example 1: Load model
#     predictor = CHDPredictor()
#     predictor.load_model()
    
#     # Example 2: Predict for a single sample
#     print("\nExample: Predicting for a single sample")
#     print("-"*70)
    
#     sample_result = predict_single_sample(
#         age=50, education=1, sex=1, is_smoking=1, cigsPerDay=20,
#         BPMeds=0, prevalentStroke=0, prevalentHyp=1, diabetes=0,
#         totChol=233, sysBP=158, diaBP=88, BMI=28,
#         heartRate=68, glucose=94
#     )

#     print(f"Prediction: {sample_result['prediction']}")
#     print(f"Risk Level: {sample_result['risk_level'].upper()}")
#     print(f"Probability of Disease: {sample_result['probability_disease']:.4f}")
#     print(f"Confidence: {sample_result['confidence']:.4f}")
    
#     # Example 3: Predict from CSV (uncomment to use)
#     # print("\nExample: Predicting from CSV file")
#     # print("-"*70)
#     # results = predict_from_csv('new_data.csv', 'predictions.csv')
#     # print(f"Predictions saved for {len(results)} samples")
    
#     print("\n" + "="*70)
#     print("Prediction completed!")
#     print("="*70)


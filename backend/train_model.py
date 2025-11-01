"""
Main Training Script for CHD Prediction
Orchestrates the complete pipeline: preprocessing, training, evaluation, and model saving
"""

import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_preprocessing import DataPreprocessor
from model_training import ModelTrainer
from evaluation import ModelEvaluator


def main():
    """Main function to run the complete pipeline"""
    
    print("="*70)
    print("CHD Prediction - Complete Training Pipeline")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Configuration
    DATA_PATH = "data\Data_cardiovascular_risk.csv"
    RANDOM_STATE = 42
    APPLY_SMOTE = True
    SAVE_MODELS = True
    SAVE_RESULTS = True
    
    # Step 1: Data Preprocessing
    print("\n" + "="*70)
    print("STEP 1: DATA PREPROCESSING")
    print("="*70)
    
    preprocessor = DataPreprocessor(
        data_path=DATA_PATH,
        random_state=RANDOM_STATE
    )
    
    X_train, X_test, y_train, y_test = preprocessor.run_full_pipeline(
        apply_smote=APPLY_SMOTE,
        save_scaler=SAVE_MODELS
    )
    
    # Step 2: Model Training
    print("\n" + "="*70)
    print("STEP 2: MODEL TRAINING")
    print("="*70)
    
    trainer = ModelTrainer(random_state=RANDOM_STATE)
    trainer.define_models()
    trainer.train_all_models(X_train, y_train, cv=5, n_jobs=-1)
    
    # Step 3: Model Evaluation
    print("\n" + "="*70)
    print("STEP 3: MODEL EVALUATION")
    print("="*70)
    
    evaluator = ModelEvaluator()
    
    # Evaluate each model
    for model_name, model in trainer.trained_models.items():
        evaluator.evaluate_model(model, X_test, y_test, model_name)
    
    # Compare all models
    comparison_df = evaluator.compare_models()
    
    # Get best model
    best_model_name, best_metrics = evaluator.get_best_model()
    
    # Step 4: Save Models and Results
    if SAVE_MODELS:
        print("\n" + "="*70)
        print("STEP 4: SAVING MODELS AND RESULTS")
        print("="*70)
        
        # Save all trained models
        trainer.save_all_models(base_path='models/')
        
        # Save the best model separately
        best_model = trainer.trained_models[best_model_name]
        trainer.save_model(best_model, best_model_name, filepath='models/best_model.pkl')
        print(f"\nBest model ({best_model_name}) saved as 'models/best_model.pkl'")
        
        # Save best model info
        import json
        best_model_info = {
            'model_name': best_model_name,
            'metrics': {
                'accuracy': float(best_metrics['accuracy']),
                'precision': float(best_metrics['precision']),
                'recall': float(best_metrics['recall']),
                'f1_score': float(best_metrics['f1_score']),
                'roc_auc': float(best_metrics.get('roc_auc', 0))
            }
        }
        os.makedirs('models', exist_ok=True)
        with open('models/best_model_info.json', 'w') as f:
            json.dump(best_model_info, f, indent=4)
        print("Best model info saved as 'models/best_model_info.json'")
        
        # Save evaluation results
        if SAVE_RESULTS:
            evaluator.save_results(filepath='results/evaluation_results.json')
    
    # Summary
    print("\n" + "="*70)
    print("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"Best Model: {best_model_name}")
    print(f"  Accuracy:  {best_metrics['accuracy']:.4f}")
    print(f"  Precision: {best_metrics['precision']:.4f}")
    print(f"  Recall:    {best_metrics['recall']:.4f}")
    print(f"  F1 Score:  {best_metrics['f1_score']:.4f}")
    print(f"  ROC AUC:   {best_metrics.get('roc_auc', 'N/A'):.4f}")
    print("\nFiles saved:")
    print("  - All models: models/")
    print("  - Best model: models/best_model.pkl")
    print("  - Best model info: models/best_model_info.json")
    print("  - Scaler: models/scaler.pkl")
    print("  - Results: results/")
    print("="*70)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please make sure the data file 'data_cardiovascular_risk.csv' exists in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



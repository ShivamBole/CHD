"""
Evaluation Metrics Module for CHD Prediction
Handles model evaluation, metrics calculation, and visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import json
import os


class ModelEvaluator:
    """Class to handle model evaluation and metrics calculation"""
    
    def __init__(self):
        """Initialize the ModelEvaluator"""
        self.results = {}
        
    def calculate_metrics(self, y_true, y_pred, model_name):
        """
        Calculate comprehensive evaluation metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            model_name: Name of the model
            
        Returns:
            Dictionary containing all metrics
        """
        metrics = {
            'model_name': model_name,
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
        
        self.results[model_name] = metrics
        
        return metrics
    
    def calculate_roc_auc(self, y_true, y_pred_proba):
        """
        Calculate ROC AUC score
        
        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities
            
        Returns:
            ROC AUC score
        """
        return roc_auc_score(y_true, y_pred_proba)
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name, save_path=None):
        """
        Plot confusion matrix
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            model_name: Name of the model
            save_path: Path to save the plot
        """
        cm = confusion_matrix(y_true, y_pred)
        conf_matrix = pd.DataFrame(
            data=cm,
            columns=['Predicted:0', 'Predicted:1'],
            index=['Actual:0', 'Actual:1']
        )
        
        plt.figure(figsize=(8, 5))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="YlGnBu")
        plt.title(f'Confusion Matrix - {model_name}')
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            print(f"Confusion matrix saved to {save_path}")
        
        plt.show()
    
    def plot_roc_curve(self, y_true, y_pred_proba, model_name, save_path=None):
        """
        Plot ROC curve
        
        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities
            model_name: Name of the model
            save_path: Path to save the plot
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
        auc = roc_auc_score(y_true, y_pred_proba)
        
        plt.figure(figsize=(10, 6))
        sns.set_style('whitegrid')
        plt.plot([0, 1], [0, 1], linestyle='--', label='Random Classifier')
        plt.plot(fpr, tpr, marker='.', label=f'{model_name} (AUC = {auc:.3f})')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend()
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            print(f"ROC curve saved to {save_path}")
        
        plt.show()
    
    def print_classification_report(self, y_true, y_pred):
        """
        Print detailed classification report
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
        """
        print("\nClassification Report:")
        print("="*50)
        print(classification_report(y_true, y_pred))
        print("="*50)
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        Comprehensive model evaluation
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            model_name: Name of the model
            
        Returns:
            Dictionary containing all evaluation results
        """
        print(f"\n{'='*50}")
        print(f"Evaluating {model_name}")
        print(f"{'='*50}")
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = self.calculate_metrics(y_test, y_pred, model_name)
        
        # Add ROC AUC
        metrics['roc_auc'] = self.calculate_roc_auc(y_test, y_pred_proba)
        
        # Print results
        print(f"\nMetrics for {model_name}:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1 Score:  {metrics['f1_score']:.4f}")
        print(f"  ROC AUC:   {metrics['roc_auc']:.4f}")
        
        # Print classification report
        self.print_classification_report(y_test, y_pred)
        
        # Plot confusion matrix
        self.plot_confusion_matrix(y_test, y_pred, model_name, 
                                   save_path=f'results/{model_name}_confusion_matrix.png')
        
        # Plot ROC curve
        self.plot_roc_curve(y_test, y_pred_proba, model_name,
                            save_path=f'results/{model_name}_roc_curve.png')
        
        return metrics
    
    def compare_models(self, save_path='results/model_comparison.csv'):
        """
        Compare all evaluated models
        
        Args:
            save_path: Path to save comparison results
        """
        if not self.results:
            print("No results to compare")
            return
        
        print("\n" + "="*50)
        print("Model Comparison")
        print("="*50)
        
        # Create comparison DataFrame
        comparison_data = []
        for model_name, metrics in self.results.items():
            comparison_data.append({
                'Model': model_name,
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1 Score': metrics['f1_score'],
                'ROC AUC': metrics.get('roc_auc', 'N/A')
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('F1 Score', ascending=False)
        
        print("\nModel Comparison Results:")
        print(comparison_df.to_string(index=False))
        
        # Save to CSV
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        comparison_df.to_csv(save_path, index=False)
        print(f"\nComparison results saved to {save_path}")
        
        # Visualize comparison
        self.plot_model_comparison(comparison_df)
        
        return comparison_df
    
    def plot_model_comparison(self, comparison_df):
        """Plot model comparison bar chart"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        
        for idx, metric in enumerate(metrics):
            ax = axes[idx // 2, idx % 2]
            comparison_df.plot(x='Model', y=metric, kind='bar', ax=ax, legend=False)
            ax.set_title(f'{metric} Comparison')
            ax.set_ylabel(metric)
            ax.set_xticklabels(comparison_df['Model'], rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig('results/model_comparison.png', dpi=300, bbox_inches='tight')
        print("Model comparison plot saved to results/model_comparison.png")
        plt.show()
    
    def save_results(self, filepath='results/evaluation_results.json'):
        """
        Save evaluation results to JSON file
        
        Args:
            filepath: Path to save results
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Convert numpy types to native Python types for JSON serialization
        json_results = {}
        for model_name, metrics in self.results.items():
            json_results[model_name] = {
                k: float(v) if isinstance(v, (np.integer, np.floating)) else v
                for k, v in metrics.items()
                if k != 'confusion_matrix'
            }
        
        with open(filepath, 'w') as f:
            json.dump(json_results, f, indent=4)
        
        print(f"Evaluation results saved to {filepath}")
    
    def get_best_model(self):
        """
        Get the best performing model based on F1 score
        
        Returns:
            Tuple of (best_model_name, best_metrics)
        """
        if not self.results:
            print("No results available")
            return None, None
        
        best_model = max(self.results.items(), key=lambda x: x[1]['f1_score'])
        
        print(f"\nBest Model: {best_model[0]}")
        print(f"  Accuracy:  {best_model[1]['accuracy']:.4f}")
        print(f"  Precision: {best_model[1]['precision']:.4f}")
        print(f"  Recall:    {best_model[1]['recall']:.4f}")
        print(f"  F1 Score:  {best_model[1]['f1_score']:.4f}")
        
        return best_model[0], best_model[1]


if __name__ == "__main__":
    # Example usage
    print("Model Evaluator Module")
    print("Import this module to evaluate your trained models")

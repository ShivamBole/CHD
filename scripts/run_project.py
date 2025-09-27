#!/usr/bin/env python3
"""
CHD Prediction Project Runner
This script runs the Jupyter notebook programmatically
"""

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def run_notebook():
    """Run the Jupyter notebook programmatically"""
    
    # Path to the notebook
    notebook_path = "CHD_Prediction_Project_Health (1).ipynb"
    
    if not os.path.exists(notebook_path):
        print(f"Error: Notebook file '{notebook_path}' not found!")
        return
    
    print("🚀 Starting CHD Prediction Project...")
    print("📊 Loading and executing notebook...")
    
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Execute the notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': '.'}})
        
        print("✅ Project executed successfully!")
        print("📈 All cells have been run and results generated.")
        
    except Exception as e:
        print(f"❌ Error running notebook: {str(e)}")
        print("💡 Try running the notebook manually in Jupyter")

if __name__ == "__main__":
    run_notebook() 
# CHD Prediction - Modular Code Structure

This directory contains a modular implementation of the CHD (Coronary Heart Disease) prediction pipeline with separate modules for data preprocessing, model training, evaluation, and model saving.

## 📁 Project Structure

```
.
├── data_preprocessing.py    # Data preprocessing pipeline
├── model_training.py       # Model training pipeline
├── evaluation.py           # Evaluation metrics and visualization
├── train_model.py          # Main script to run complete pipeline
├── requirements.txt        # Python dependencies
└── README_MODULAR.md       # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Complete Pipeline

```bash
python train_model.py
```

This will:
- Load and preprocess the data
- Train multiple models with hyperparameter tuning
- Evaluate all models
- Save the best model and results

## 📊 Module Details

### 1. Data Preprocessing (`data_preprocessing.py`)

**Class: `DataPreprocessor`**

Handles all data preprocessing operations:
- Data loading
- Missing value handling
- Categorical feature encoding
- SMOTE for balancing dataset
- Train-test split
- Feature scaling
- Scaler saving

**Usage:**
```python
from data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor(data_path="data_cardiovascular_risk.csv")
X_train, X_test, y_train, y_test = preprocessor.run_full_pipeline()
```

### 2. Model Training (`model_training.py`)

**Class: `ModelTrainer`**

Handles model training and hyperparameter tuning:
- Defines multiple models (Logistic Regression, KNN, Decision Tree, Random Forest, SVM)
- Performs GridSearchCV for hyperparameter tuning
- Trains all models
- Saves trained models

**Usage:**
```python
from model_training import ModelTrainer

trainer = ModelTrainer()
trainer.define_models()
trainer.train_all_models(X_train, y_train)
trainer.save_all_models()
```

### 3. Evaluation (`evaluation.py`)

**Class: `ModelEvaluator`**

Handles model evaluation:
- Calculates comprehensive metrics (accuracy, precision, recall, F1, ROC AUC)
- Plots confusion matrices
- Plots ROC curves
- Compares all models
- Saves evaluation results

**Usage:**
```python
from evaluation import ModelEvaluator

evaluator = ModelEvaluator()
evaluator.evaluate_model(model, X_test, y_test, "ModelName")
evaluator.compare_models()
evaluator.save_results()
```

### 4. Main Training Script (`train_model.py`)

Orchestrates the complete pipeline:
- Runs data preprocessing
- Trains all models
- Evaluates models
- Saves models and results

**Usage:**
```bash
python train_model.py
```

## 📈 Models Included

1. **Logistic Regression** - Linear classifier
2. **K-Nearest Neighbors** - Instance-based learning
3. **Decision Tree** - Tree-based classifier
4. **Random Forest** - Ensemble of decision trees
5. **Support Vector Machine** - Kernel-based classifier

## 📁 Output Files

After running the pipeline, you'll find:

```
models/
├── LogisticRegression.pkl
├── KNeighborsClassifier.pkl
├── DecisionTreeClassifier.pkl
├── RandomForestClassifier.pkl
├── SVC.pkl
└── scaler.pkl

results/
├── evaluation_results.json
├── model_comparison.csv
├── model_comparison.png
└── [model_name]_confusion_matrix.png
└── [model_name]_roc_curve.png
```

## 🔧 Customization

### Modify Models

Edit `model_training.py` to add/remove models or change hyperparameters:

```python
self.models = {
    'YourModel': {
        'model': YourModelClass(),
        'params': {
            'param1': [value1, value2],
            'param2': [value3, value4]
        }
    }
}
```

### Modify Preprocessing

Edit `data_preprocessing.py` to customize preprocessing steps:

```python
def custom_preprocessing_step(self):
    # Your custom preprocessing logic
    pass
```

### Modify Evaluation Metrics

Edit `evaluation.py` to add custom metrics:

```python
def calculate_custom_metric(self, y_true, y_pred):
    # Your custom metric calculation
    pass
```

## 📝 Example: Using Individual Modules

### Load Preprocessed Data

```python
from data_preprocessing import DataPreprocessor

preprocessor = DataPreprocessor(data_path="data.csv")
X_train, X_test, y_train, y_test = preprocessor.run_full_pipeline()
```

### Train a Single Model

```python
from model_training import ModelTrainer

trainer = ModelTrainer()
trainer.define_models()
model = trainer.train_model("RandomForestClassifier", X_train, y_train)
```

### Evaluate a Model

```python
from evaluation import ModelEvaluator

evaluator = ModelEvaluator()
metrics = evaluator.evaluate_model(model, X_test, y_test, "RandomForest")
```

## 🎯 Key Features

- **Modular Design**: Each component is independent and reusable
- **Comprehensive Evaluation**: Multiple metrics and visualizations
- **Model Persistence**: All models are saved for future use
- **Hyperparameter Tuning**: GridSearchCV for optimal parameters
- **Class Imbalance Handling**: SMOTE for balanced training
- **Feature Scaling**: StandardScaler for consistent features
- **Results Visualization**: Confusion matrices and ROC curves

## 📊 Evaluation Metrics

- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall
- **ROC AUC**: Area under the ROC curve

## 🔍 Model Selection

The best model is selected based on F1 score, which is ideal for imbalanced datasets as it considers both precision and recall.

## 📚 Dependencies

See `requirements.txt` for complete list of dependencies.

## 🤝 Contributing

Feel free to extend the modules with additional features:
- More models
- Additional evaluation metrics
- Custom preprocessing steps
- Advanced visualization

## 📄 License

This project is for educational purposes.

## 👤 Author

Created for CHD Prediction Project
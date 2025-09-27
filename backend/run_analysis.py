#!/usr/bin/env python3
"""
CHD Prediction Analysis Runner
Direct Python script to run the cardiovascular disease prediction analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load the cardiovascular dataset"""
    print("📊 Loading cardiovascular dataset...")
    try:
        df = pd.read_csv('Data_cardiovascular_risk.csv')
        print(f"✅ Dataset loaded successfully! Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

def explore_data(df):
    """Perform exploratory data analysis"""
    print("\n🔍 Exploratory Data Analysis")
    print("=" * 50)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nTarget variable 'TenYearCHD' distribution:")
    print(df['TenYearCHD'].value_counts())
    
    print(f"\nMissing values:")
    print(df.isnull().sum())
    
    print(f"\nData types:")
    print(df.dtypes)
    
    # Basic statistics
    print(f"\nBasic statistics:")
    print(df.describe())

def visualize_data(df):
    """Create visualizations"""
    print("\n📈 Creating visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create a figure with multiple subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Cardiovascular Disease Risk Analysis', fontsize=16)
    
    # 1. Age distribution
    axes[0,0].hist(df['age'], bins=20, alpha=0.7, color='skyblue')
    axes[0,0].set_title('Age Distribution')
    axes[0,0].set_xlabel('Age')
    axes[0,0].set_ylabel('Frequency')
    
    # 2. Gender distribution
    df['sex'].value_counts().plot(kind='bar', ax=axes[0,1], color='lightcoral')
    axes[0,1].set_title('Gender Distribution')
    axes[0,1].set_xlabel('Gender')
    axes[0,1].set_ylabel('Count')
    
    # 3. Smoking status
    df['is_smoking'].value_counts().plot(kind='bar', ax=axes[0,2], color='lightgreen')
    axes[0,2].set_title('Smoking Status')
    axes[0,2].set_xlabel('Smoking')
    axes[0,2].set_ylabel('Count')
    
    # 4. BMI distribution
    axes[1,0].hist(df['BMI'].dropna(), bins=20, alpha=0.7, color='gold')
    axes[1,0].set_title('BMI Distribution')
    axes[1,0].set_xlabel('BMI')
    axes[1,0].set_ylabel('Frequency')
    
    # 5. Target variable distribution
    df['TenYearCHD'].value_counts().plot(kind='bar', ax=axes[1,1], color='lightblue')
    axes[1,1].set_title('CHD Risk Distribution')
    axes[1,1].set_xlabel('Ten Year CHD Risk')
    axes[1,1].set_ylabel('Count')
    
    # 6. Correlation heatmap for numeric variables
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=axes[1,2])
    axes[1,2].set_title('Correlation Matrix')
    
    plt.tight_layout()
    plt.savefig('cardiovascular_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Visualizations saved as 'cardiovascular_analysis.png'")

def prepare_data(df):
    """Prepare data for machine learning"""
    print("\n🔧 Preparing data for machine learning...")
    
    # Handle missing values
    df_clean = df.copy()
    
    # Fill missing values with median for numeric columns
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    # Convert categorical variables
    df_clean['sex'] = df_clean['sex'].map({'M': 1, 'F': 0})
    df_clean['is_smoking'] = df_clean['is_smoking'].map({'YES': 1, 'NO': 0})
    
    # Select features for modeling
    feature_cols = ['age', 'sex', 'is_smoking', 'cigsPerDay', 'BPMeds', 
                   'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 
                   'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
    
    X = df_clean[feature_cols]
    y = df_clean['TenYearCHD']
    
    print(f"✅ Data prepared! Features: {len(feature_cols)}, Samples: {len(X)}")
    return X, y

def train_models(X, y):
    """Train machine learning models"""
    print("\n🤖 Training machine learning models...")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = {
            'accuracy': accuracy,
            'predictions': y_pred,
            'model': model
        }
        
        print(f"✅ {name} - Accuracy: {accuracy:.4f}")
    
    return results, X_test, y_test

def evaluate_models(results, X_test, y_test):
    """Evaluate model performance"""
    print("\n📊 Model Evaluation Results")
    print("=" * 50)
    
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"Accuracy: {result['accuracy']:.4f}")
        
        # Classification report
        print("Classification Report:")
        print(classification_report(y_test, result['predictions']))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, result['predictions'])
        print("Confusion Matrix:")
        print(cm)

def main():
    """Main function to run the analysis"""
    print("🚀 CHD Prediction Project - Cardiovascular Disease Risk Analysis")
    print("=" * 70)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Explore data
    explore_data(df)
    
    # Create visualizations
    visualize_data(df)
    
    # Prepare data
    X, y = prepare_data(df)
    
    # Train models
    results, X_test, y_test = train_models(X, y)
    
    # Evaluate models
    evaluate_models(results, X_test, y_test)
    
    print("\n🎉 Analysis completed successfully!")
    print("📁 Check 'cardiovascular_analysis.png' for visualizations")

if __name__ == "__main__":
    main() 
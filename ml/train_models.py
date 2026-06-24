import os
import sys
import pandas as pd
import numpy as np
import re
import string
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.cluster import KMeans

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'datasets', 'kaggle_resume_dataset.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

def clean_resume_text(text):
    """
    Cleans long-form contextual text:
    - Lowers text
    - Removes URLs, emails
    - Removes punctuation and extra whitespace
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_and_save_models():
    print("=" * 60)
    print("  Career Lens — Training on Kaggle Resume Dataset")
    print("=" * 60)
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}")
        return
        
    print("1. Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    if 'Category' not in df.columns or 'Resume' not in df.columns:
        print("Error: Dataset must contain 'Category' and 'Resume' columns.")
        return
        
    df = df.dropna(subset=['Category', 'Resume'])
    print(f"Loaded {len(df)} records.")
    
    print("\n2. Cleaning text...")
    df['Clean_Resume'] = df['Resume'].apply(clean_resume_text)
    
    print("\n3. Encoding labels...")
    le = LabelEncoder()
    df['Category_Encoded'] = le.fit_transform(df['Category'])
    joblib.dump(le, os.path.join(MODELS_DIR, 'label_encoder.pkl'))
    print(f"Classes found: {len(le.classes_)}")
    
    print("\n4. Vectorizing contextual text (TF-IDF)...")
    # Using 1-2 ngrams for better context capture on long-form text
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['Clean_Resume'])
    y = df['Category_Encoded']
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, 'vectorizer.pkl'))
    print(f"TF-IDF matrix shape: {X.shape}")
    
    print("\n5. Clustering (K-Means)...")
    clusterer = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusterer.fit(X)
    joblib.dump(clusterer, os.path.join(MODELS_DIR, 'clusterer.pkl'))
    print("Clustering model saved.")
    
    print("\n6. Training Classification Model with Cross-Validation...")
    # Logistic Regression is highly effective and fast for high-dimensional TF-IDF text features
    model = LogisticRegression(max_iter=1000, C=10, random_state=42)
    
    # Rigorous cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    print(f"Cross-Validation Accuracy: {np.mean(cv_scores)*100:.2f}% (+/- {np.std(cv_scores)*100:.2f}%)")
    
    # Final Model Training
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    test_acc = accuracy_score(y_test, y_pred)
    print(f"\nFinal Test Accuracy: {test_acc*100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save Model
    joblib.dump(model, os.path.join(MODELS_DIR, 'classifier.pkl'))
    print(f"\n✅ All models saved successfully to {MODELS_DIR}/")

if __name__ == '__main__':
    train_and_save_models()

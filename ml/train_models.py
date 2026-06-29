import os
import pandas as pd
import numpy as np
import re
import string
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.cluster import KMeans

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'datasets', 'kaggle_resume_dataset.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(MODELS_DIR, exist_ok=True)

def clean_resume_text(text):
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
    print("  Career Lens — Training on Kaggle Resume Dataset")
    
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
    
    print("\n4. Splitting Data and Vectorizing (TF-IDF)...")
    text_train, text_test, y_train, y_test = train_test_split(
        df['Clean_Resume'], df['Category_Encoded'], test_size=0.2, random_state=42, stratify=df['Category_Encoded']
    )
    
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(text_train)
    X_test = vectorizer.transform(text_test)
    print(f"TF-IDF training matrix shape: {X_train.shape}")
    
    print("\n5. Evaluating Classification Model with Cross-Validation...")
    model = LogisticRegression(max_iter=1000, C=10, random_state=42)
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
    print(f"Cross-Validation Accuracy: {np.mean(cv_scores)*100:.2f}% (+/- {np.std(cv_scores)*100:.2f}%)")
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    test_acc = accuracy_score(y_test, y_pred)
    print(f"\nFinal Test Accuracy (Unbiased): {test_acc*100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    print("\n6. Retraining on Full Dataset & Clustering...")
    X_full = vectorizer.fit_transform(df['Clean_Resume'])
    model.fit(X_full, df['Category_Encoded'])
    
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, 'vectorizer.pkl'))
    joblib.dump(model, os.path.join(MODELS_DIR, 'classifier.pkl'))
    
    clusterer = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusterer.fit(X_full)
    joblib.dump(clusterer, os.path.join(MODELS_DIR, 'clusterer.pkl'))
    
    print(f"\n All models saved successfully to {MODELS_DIR}/")

if __name__ == '__main__':
    train_and_save_models()

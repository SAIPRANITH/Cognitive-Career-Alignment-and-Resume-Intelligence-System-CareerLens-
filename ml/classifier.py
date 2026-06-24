"""
Classification Module
Demonstrates: Logistic Regression, Random Forest, XGBoost comparison,
accuracy metrics, prediction with probability scores.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, classification_report, confusion_matrix)
from sklearn.preprocessing import StandardScaler
import joblib
import os

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False


class ResumeClassifier:
    """Train and compare multiple classifiers for job category prediction."""

    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.best_model_name = None
        self.best_model = None
        self.label_classes = None
        self.feature_names = None
        self.metrics = {}
        self.is_trained = False

    def train(self, X, y, feature_names, label_classes, test_size=0.2):
        """Train all models and compare performance."""
        self.feature_names = feature_names
        self.label_classes = label_classes

        # ── Split data ──
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # ── Scale features ──
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # ── Define models ──
        classifiers = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=42, multi_class='multinomial'
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=100, random_state=42, max_depth=15, n_jobs=-1
            ),
        }

        if HAS_XGBOOST:
            classifiers['XGBoost'] = XGBClassifier(
                n_estimators=100, random_state=42, max_depth=6,
                learning_rate=0.1, eval_metric='mlogloss',
                use_label_encoder=False
            )
        else:
            classifiers['Gradient Boosting'] = GradientBoostingClassifier(
                n_estimators=100, random_state=42, max_depth=6, learning_rate=0.1
            )

        # ── Train & evaluate each model ──
        best_acc = 0
        for name, clf in classifiers.items():
            clf.fit(X_train_scaled, y_train)
            y_pred = clf.predict(X_test_scaled)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

            # Cross-validation
            cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=5, scoring='accuracy')

            self.models[name] = clf
            self.metrics[name] = {
                'accuracy': round(acc * 100, 2),
                'precision': round(prec * 100, 2),
                'recall': round(rec * 100, 2),
                'f1_score': round(f1 * 100, 2),
                'cv_mean': round(cv_scores.mean() * 100, 2),
                'cv_std': round(cv_scores.std() * 100, 2),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'classification_report': classification_report(
                    y_test, y_pred, target_names=label_classes, output_dict=True, zero_division=0
                )
            }

            if acc > best_acc:
                best_acc = acc
                self.best_model_name = name
                self.best_model = clf

        self.X_test = X_test_scaled
        self.y_test = y_test
        self.is_trained = True

        return self.metrics

    def predict(self, X):
        """Predict job categories with probabilities."""
        X_scaled = self.scaler.transform(X)
        predictions = self.best_model.predict(X_scaled)
        probabilities = self.best_model.predict_proba(X_scaled)
        return predictions, probabilities

    def predict_top_roles(self, X, top_n=5):
        """Get top N predicted roles with their probabilities."""
        X_scaled = self.scaler.transform(X)
        probabilities = self.best_model.predict_proba(X_scaled)[0]

        # ── Sort by probability ──
        top_indices = np.argsort(probabilities)[::-1][:top_n]

        results = []
        for idx in top_indices:
            results.append({
                'role': self.label_classes[idx],
                'probability': round(probabilities[idx] * 100, 2)
            })
        return results

    def check_specific_role(self, X, target_role):
        """Check probability for a specific target role."""
        X_scaled = self.scaler.transform(X)
        probabilities = self.best_model.predict_proba(X_scaled)[0]

        if target_role in self.label_classes:
            idx = list(self.label_classes).index(target_role)
            return round(probabilities[idx] * 100, 2)
        return 0.0

    def get_feature_importance(self):
        """Get feature importance from the best model."""
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            pairs = sorted(zip(self.feature_names, importances),
                          key=lambda x: x[1], reverse=True)
            return {name: round(float(imp), 4) for name, imp in pairs}
        return {}

    def get_model_comparison(self):
        """Return a comparison table of all models."""
        rows = []
        for name, m in self.metrics.items():
            rows.append({
                'Model': name,
                'Accuracy': f"{m['accuracy']}%",
                'Precision': f"{m['precision']}%",
                'Recall': f"{m['recall']}%",
                'F1 Score': f"{m['f1_score']}%",
                'CV Mean': f"{m['cv_mean']}%",
                'Best': '✅' if name == self.best_model_name else ''
            })
        return rows

    def save_model(self, path):
        """Save trained model and scaler."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {
            'best_model': self.best_model,
            'best_model_name': self.best_model_name,
            'scaler': self.scaler,
            'label_classes': self.label_classes,
            'feature_names': self.feature_names,
            'metrics': self.metrics,
            'all_models': self.models
        }
        joblib.dump(data, path)

    def load_model(self, path):
        """Load trained model and scaler."""
        data = joblib.load(path)
        self.best_model = data['best_model']
        self.best_model_name = data['best_model_name']
        self.scaler = data['scaler']
        self.label_classes = data['label_classes']
        self.feature_names = data['feature_names']
        self.metrics = data['metrics']
        self.models = data.get('all_models', {self.best_model_name: self.best_model})
        self.is_trained = True
        return self

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import pickle

def build_features(sessions):
    rows = []
    for s in sessions:
        emo = s.get('emotions', {})
        rows.append({
            'score': s.get('score', 50),
            'duration': s.get('duration', 0),
            'hour': s.get('hour', 12),
            'stress': emo.get('stress', 0),
            'confusion': emo.get('confusion', 0),
            'boreout': emo.get('boreout', 0),
            'engagement': emo.get('engagement', 50),
            'label': s.get('label_burnout', 0)
        })
    return pd.DataFrame(rows)

def main():
    with open('training_data_final.json') as f:
        sessions = json.load(f)
    
    df = build_features(sessions)
    X = df.drop('label', axis=1)
    y = df['label']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'Neural Network (MLP)': MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=1000, random_state=42)
    }
    
    results = []
    best_model = None
    best_score = 0
    
    for name, model in models.items():
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, preds)
        try:
            auc = roc_auc_score(y_test, probs)
        except:
            auc = None
        
        results.append({
            'model': name,
            'cv_accuracy_mean': round(cv_scores.mean(), 3),
            'cv_accuracy_std': round(cv_scores.std(), 3),
            'test_accuracy': round(acc, 3),
            'test_auc': round(auc, 3) if auc else None
        })
        
        if acc > best_score:
            best_score = acc
            best_model = model
            best_name = name
    
    print("\n=== MODEL COMPARISON ===")
    for r in results:
        print(r)
    
    print(f"\nBest model: {best_name} (test accuracy: {best_score})")
    
    # Save the winner + the scaler (you need both at inference time)
    with open('fatigue_model.pkl', 'wb') as f:
        pickle.dump({'model': best_model, 'scaler': scaler, 'name': best_name}, f)
    
    with open('model_comparison_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Saved fatigue_model.pkl and model_comparison_results.json")

if __name__ == '__main__':
    main()
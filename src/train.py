import os
import time
import pandas as pd
import joblib

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from utils import PROCESSED_DATA_DIR, MODELS_DIR

def load_train_data():
    train_path = os.path.join(PROCESSED_DATA_DIR, "train_features.csv")
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Processed training data not found at {train_path}.")
    
    print(f"Loading training data from {train_path}...")
    df = pd.read_csv(train_path)
    X = df.drop(columns=['label'])
    y = df['label']
    print(f"Features shape: {X.shape}, Target distribution: Phishing: {sum(y == 1)}, Legitimate: {sum(y == 0)}")
    return X, y

def train_and_save_models():
    X_train, y_train = load_train_data()

    models = {
        "baseline": DummyClassifier(strategy="most_frequent"),
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1),
        "xgboost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1)
    }
    
    for name, model in models.items():
        print(f"\nTraining model: {name.upper()}...")
        start_time = time.time()

        model.fit(X_train, y_train)
        
        elapsed_time = time.time() - start_time
        print(f"Finished training {name.upper()} in {elapsed_time:.2f} seconds.")

        model_path = os.path.join(MODELS_DIR, f"{name}.joblib")
        joblib.dump(model, model_path)
        print(f"Saved {name.upper()} model to {model_path}")
        
    print("\nAll models trained and saved successfully.")

if __name__ == "__main__":
    train_and_save_models()

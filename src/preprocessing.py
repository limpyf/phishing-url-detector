import os
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

from utils import LOCAL_RAW_PATH, PROCESSED_DATA_DIR, MODELS_DIR
from feature_engineering import extract_features_from_url

def load_raw_data():
    if not os.path.exists(LOCAL_RAW_PATH):
        raise FileNotFoundError(f"Raw dataset not found at {LOCAL_RAW_PATH}. Please ensure the PhiUSIIL_Phishing_URL_Dataset.csv dataset file is placed inside the data/raw/ directory.")
    
    print(f"Loading raw dataset from {LOCAL_RAW_PATH}...")
    df = pd.read_csv(LOCAL_RAW_PATH, usecols=['URL', 'label'])
    print(f"Loaded {len(df):,} samples.")
    return df

def preprocess_and_save():
    df = load_raw_data()

    initial_count = len(df)
    df = df.dropna(subset=['URL', 'label'])
    final_count = len(df)
    if initial_count != final_count:
        print(f"Removed {initial_count - final_count} rows with missing values.")

    df['label'] = 1 - df['label']

    print("Extracting handcrafted features from URLs.")
    start_time = time.time()

    urls = df['URL'].tolist()

    extracted_features = []
    total_urls = len(urls)
    for i, url in enumerate(urls):
        extracted_features.append(extract_features_from_url(url))
        if (i + 1) % 50000 == 0 or (i + 1) == total_urls:
            print(f"Processed {i + 1}/{total_urls} URLs...")
            
    features_df = pd.DataFrame(extracted_features)

    features_df['label'] = df['label'].values
    
    elapsed_time = time.time() - start_time
    print(f"Feature extraction completed in {elapsed_time:.2f} seconds.")

    X = features_df.drop(columns=['label'])
    y = features_df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    numerical_cols = [
        'url_length', 'qty_digits', 'qty_dots', 'qty_hyphens', 
        'qty_subdomains', 'qty_special_chars'
    ]
    
    print("Scaling numerical features...")
    scaler = StandardScaler()

    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
    X_test_scaled[numerical_cols] = scaler.transform(X_test[numerical_cols])

    scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

    train_data = X_train_scaled.copy()
    train_data['label'] = y_train
    
    test_data = X_test_scaled.copy()
    test_data['label'] = y_test

    train_path = os.path.join(PROCESSED_DATA_DIR, "train_features.csv")
    test_path = os.path.join(PROCESSED_DATA_DIR, "test_features.csv")
    
    print(f"Saving processed train data to {train_path}...")
    train_data.to_csv(train_path, index=False)
    
    print(f"Saving processed test data to {test_path}...")
    test_data.to_csv(test_path, index=False)
    
    print("Data preprocessing completed successfully.")
    
if __name__ == "__main__":
    preprocess_and_save()

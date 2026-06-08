import os
import sys
import argparse
import joblib
import pandas as pd
import numpy as np

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from utils import MODELS_DIR
from feature_engineering import extract_features_from_url

def print_indicator(desc):
    try:
        print(f" ✓ {desc}")
    except UnicodeEncodeError:
        print(f" [+] {desc}")

def predict_url(url):
    raw_features = extract_features_from_url(url)

    feature_order = [
        'url_length', 'qty_digits', 'qty_dots', 'qty_hyphens', 'is_https', 'is_ip',
        'qty_subdomains', 'qty_special_chars', 'keyword_login', 'keyword_verify',
        'keyword_secure', 'keyword_update', 'keyword_account', 'keyword_password',
        'keyword_banking', 'keyword_confirm'
    ]
    
    df_feats = pd.DataFrame([raw_features])[feature_order]

    scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
    if not os.path.exists(scaler_path):
        print("ERROR: Scaler file not found. Please run preprocessing first.")
        return False
        
    scaler = joblib.load(scaler_path)
    numerical_cols = [
        'url_length', 'qty_digits', 'qty_dots', 'qty_hyphens', 
        'qty_subdomains', 'qty_special_chars'
    ]
    df_feats[numerical_cols] = scaler.transform(df_feats[numerical_cols])

    best_model_path = os.path.join(MODELS_DIR, "best_model.joblib")
    if not os.path.exists(best_model_path):
        best_model_path = os.path.join(MODELS_DIR, "xgboost.joblib")
        if not os.path.exists(best_model_path):
            print("ERROR: No trained model found. Please run --train first.")
            return False
            
    model = joblib.load(best_model_path)

    pred = model.predict(df_feats)[0]

    prob = None
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(df_feats)[0]

    color_red = "\033[91m"
    color_green = "\033[92m"
    color_bold = "\033[1m"
    color_reset = "\033[0m"
    
    if pred == 1:
        pred_label = f"{color_red}{color_bold}PHISHING{color_reset}"
        confidence = prob[1] if prob is not None else 1.0
    else:
        pred_label = f"{color_green}{color_bold}LEGITIMATE{color_reset}"
        confidence = prob[0] if prob is not None else 1.0
        
    print(f"Prediction: {pred_label}\n")
    print(f"Confidence: {confidence * 100:.1f}%\n")
    print("Detected indicators:")
    
    has_indicators = False

    indicators_map = [
        ('keyword_login', "contains_login"),
        ('keyword_verify', "contains_verify"),
        ('keyword_secure', "contains_secure"),
        ('keyword_update', "contains_update"),
        ('keyword_account', "contains_account"),
        ('keyword_password', "contains_password"),
        ('keyword_banking', "contains_banking"),
        ('keyword_confirm', "contains_confirm"),
    ]

    for key, desc in indicators_map:
        if raw_features[key] == 1:
            print_indicator(desc)
            has_indicators = True

    if raw_features['qty_hyphens'] > 1:
        print_indicator(f"multiple_hyphens ({raw_features['qty_hyphens']} hyphens)")
        has_indicators = True
        
    if raw_features['url_length'] > 75:
        print_indicator(f"long_url ({raw_features['url_length']} chars)")
        has_indicators = True
        
    if raw_features['is_https'] == 0:
        print_indicator("insecure_protocol (HTTP)")
        has_indicators = True
        
    if raw_features['is_ip'] == 1:
        print_indicator("raw_ip_address")
        has_indicators = True
        
    if raw_features['qty_dots'] > 3:
        print_indicator(f"multiple_dots ({raw_features['qty_dots']} dots)")
        has_indicators = True
        
    if raw_features['qty_subdomains'] > 1:
        print_indicator(f"multiple_subdomains ({raw_features['qty_subdomains']} subdomains)")
        has_indicators = True
        
    if not has_indicators:
        print("  None (No common suspicious patterns detected)")
        
    print("=" * 60)
    return True

def main():
    parser = argparse.ArgumentParser(description="Predict if a URL is Phishing or Legitimate.")
    parser.add_argument("--url", type=str, required=True, help="The URL to analyze")
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"PHISHING URL DETECTOR - ANALYSIS")
    print("=" * 60)
    print(f"Target URL: {args.url}\n")
    predict_url(args.url)

if __name__ == "__main__":
    main()

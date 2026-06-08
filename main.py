import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.utils import setup_directories
from src.preprocessing import preprocess_and_save
from src.train import train_and_save_models
from src.evaluate import evaluate_models
from src.predict import predict_url

def main():
    parser = argparse.ArgumentParser(
        description="Unified Entry Point - Phishing URL Detector"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--train", 
        action="store_true", 
        help="Run preprocessing, train all models, evaluate, and save the best model."
    )
    group.add_argument(
        "--evaluate", 
        action="store_true", 
        help="Load saved models and regenerate all evaluation metrics and plots."
    )
    group.add_argument(
        "--predict", 
        type=str, 
        metavar="URL",
        help="Predict if the specified URL is Phishing or Legitimate using the best model."
    )
    
    args = parser.parse_args()

    setup_directories()
    
    if args.train:
        print("\n" + "=" * 60)
        print("PHASE 1 - DATA PREPROCESSING")
        print("=" * 60)
        preprocess_and_save()
        
        print("\n" + "=" * 60)
        print("PHASE 2 - MODEL TRAINING")
        print("=" * 60)
        train_and_save_models()
        
        print("\n" + "=" * 60)
        print("PHASE 3 - EVALUATION, VISUALIZATION, and BEST MODEL SELECTION")
        print("=" * 60)
        evaluate_models()
        print("\nTraining and pipeline execution completed successfully.")
        
    elif args.evaluate:
        print("\n" + "=" * 60)
        print("PIPELINE RE-EVALUATION and VISUALIZATION")
        print("=" * 60)
        try:
            evaluate_models()
            print("\nRe-evaluation completed successfully.")
        except FileNotFoundError as e:
            print(f"\nERROR: {e}")
            print("Please run with --train first to build features and train models.")
            
    elif args.predict:
        url = args.predict
        print("=" * 60)
        print(f"PHISHING URL DETECTOR - ANALYSIS")
        print("=" * 60)
        print(f"Target URL: {url}\n")
        
        success = predict_url(url)
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()

# Project Structure

This document provides a directory map of the **Phishing URL Detector** repository to help developers and reviewers navigate the codebase.

```text
phishing-url-detector/
├── assets/
│   └── plots/                       # Model evaluation charts & graphs
│       ├── class_distribution.png
│       ├── confusion_matrix_*.png   # Confusion matrices for each classifier
│       ├── feature_importance_*.png # Relative feature & permutation importances
│       ├── model_comparison.png     # Metric comparison bar chart
│       ├── precision_recall_curve.png
│       └── roc_curve_comparison.png
├── data/
│   ├── raw/
│   │   ├── .gitkeep
│   │   └── PhiUSIIL_Phishing_URL_Dataset.csv # Raw input dataset (ignored in git)
│   └── processed/
│       ├── .gitkeep
│       ├── test_features.csv       # Extracted test set features (ignored)
│       ├── train_features.csv      # Extracted train set features (ignored)
│       └── evaluation_results.md   # Automatic summary of model benchmarks
├── docs/
│   └── DATASET_DESCRIPTION.md      # Detailed description of the PhiUSIIL dataset
├── models/
│   ├── .gitkeep
│   ├── baseline.joblib             # Serialized dummy baseline model (ignored)
│   ├── best_model.joblib           # Copy of the best classifier (XGBoost) (ignored)
│   ├── logistic_regression.joblib  # Serialized Logistic Regression model (ignored)
│   ├── random_forest.joblib        # Serialized Random Forest classifier (ignored)
│   ├── scaler.joblib               # Fitted StandardScaler object (ignored)
│   └── xgboost.joblib              # Serialized XGBoost model (ignored)
├── reports/
│   └── experiments/
│       └── benchmark_summary.md    # Experiment history and developer notes
├── src/
│   ├── evaluate.py                 # Core evaluation, metrics, and plotting script
│   ├── feature_engineering.py      # Lexical and keyword URL feature extraction
│   ├── predict.py                  # Live URL inference script & CLI utility
│   ├── preprocessing.py            # Dataset cleaning, inversion, and scaling logic
│   ├── train.py                    # Training script for all 4 models
│   └── utils.py                    # File paths and folder management utilities
├── .gitignore                      # Specified exclusions for large data/model files
├── README.md                       # Main portfolio landing page
└── requirements.txt                # Production dependency list
```

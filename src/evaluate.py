import os
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix
)

from utils import PROCESSED_DATA_DIR, MODELS_DIR, PLOTS_DIR

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'font.family': 'sans-serif'
})

COLORS = {
    "baseline": "#7f8c8d",
    "logistic_regression": "#3498db",
    "random_forest": "#2ecc71",
    "xgboost": "#e67e22"
}

def load_test_data():
    test_path = os.path.join(PROCESSED_DATA_DIR, "test_features.csv")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Processed test data not found at {test_path}.")
    
    print(f"Loading test data from {test_path}...")
    df = pd.read_csv(test_path)
    X = df.drop(columns=['label'])
    y = df['label']
    return X, y

def load_models():
    models = {}
    model_names = ["baseline", "logistic_regression", "random_forest", "xgboost"]
    for name in model_names:
        model_path = os.path.join(MODELS_DIR, f"{name}.joblib")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}.")
        models[name] = joblib.load(model_path)
    return models

def evaluate_models():
    X_test, y_test = load_test_data()
    models = load_models()

    plot_class_distribution(y_test)
    
    results = []
    roc_curves_data = {}
    feature_importances = {}
    
    best_name = None
    best_auc = -1.0
    best_model_obj = None
    
    for name, model in models.items():
        print(f"Evaluating {name.upper()}...")

        y_pred = model.predict(X_test)

        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        elif hasattr(model, "decision_function"):
            y_prob = model.decision_function(X_test)
        else:
            y_prob = y_pred.astype(float)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        try:
            auc = roc_auc_score(y_test, y_prob)
        except Exception:
            auc = 0.5

        if name != "baseline" and auc > best_auc:
            best_auc = auc
            best_name = name
            best_model_obj = model
            
        results.append({
            "Model": name.upper().replace("_", " "),
            "Accuracy": f"{acc:.4f}",
            "Precision": f"{prec:.4f}",
            "Recall": f"{rec:.4f}",
            "F1 Score": f"{f1:.4f}",
            "ROC-AUC": f"{auc:.4f}"
        })

        try:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_curves_data[name] = (fpr, tpr, auc)
        except Exception:
            roc_curves_data[name] = (np.array([0, 1]), np.array([0, 1]), 0.5)

        plot_confusion_matrix(y_test, y_pred, name)

        if name == "random_forest":
            feature_importances[name] = model.feature_importances_
        elif name == "xgboost":
            feature_importances[name] = model.feature_importances_

    results_df = pd.DataFrame(results)
    print("\nEvaluation Summary:")
    print(results_df.to_string(index=False))

    md_table = results_df.to_markdown(index=False)
    results_path = os.path.join(PROCESSED_DATA_DIR, "evaluation_results.md")
    with open(results_path, "w") as f:
        f.write("# Model Evaluation Results\n\n")
        f.write(md_table)
    print(f"\nSaved comparison table to {results_path}")

    if best_model_obj is not None:
        best_model_path = os.path.join(MODELS_DIR, "best_model.joblib")
        joblib.dump(best_model_obj, best_model_path)
        print(f"Best Model Selected: {best_name.upper().replace('_', ' ')} (ROC-AUC: {best_auc:.4f})")
        print(f"Saved best model to {best_model_path}")

    plot_roc_curves(roc_curves_data)

    if feature_importances:
        plot_feature_importances(feature_importances, list(X_test.columns))

def plot_class_distribution(y_test):
    plt.figure(figsize=(7, 5))
    counts = y_test.value_counts()
    labels = ['Phishing (1)', 'Legitimate (0)']
    values = [counts.get(1, 0), counts.get(0, 0)]
    
    colors = ['#e74c3c', '#2c3e50']
    
    bars = plt.bar(labels, values, color=colors, width=0.5, edgecolor='grey', alpha=0.95)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + (max(values)*0.01), 
                 f"{yval:,}\n({yval/len(y_test)*100:.1f}%)", 
                 ha='center', va='bottom', fontweight='bold')
                 
    plt.title("Class Distribution in Test Dataset", pad=15)
    plt.ylabel("Number of Samples")
    plt.ylim(0, max(values) * 1.15)
    plt.tight_layout()
    
    plot_path = os.path.join(PLOTS_DIR, "class_distribution.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved class distribution plot to {plot_path}")

def plot_confusion_matrix(y_true, y_pred, model_name):
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(6, 5))

    if model_name == "baseline":
        cmap = sns.light_palette("#7f8c8d", as_cmap=True)
    elif model_name == "logistic_regression":
        cmap = sns.light_palette("#3498db", as_cmap=True)
    elif model_name == "random_forest":
        cmap = sns.light_palette("#2ecc71", as_cmap=True)
    else:
        cmap = sns.light_palette("#e67e22", as_cmap=True)
        
    sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, cbar=False,
                xticklabels=["Legitimate (0)", "Phishing (1)"],
                yticklabels=["Legitimate (0)", "Phishing (1)"],
                annot_kws={"size": 14, "weight": "bold"})
                
    plt.title(f"Confusion Matrix - {model_name.upper().replace('_', ' ')}", pad=15)
    plt.ylabel("Actual Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    
    plot_path = os.path.join(PLOTS_DIR, f"confusion_matrix_{model_name}.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved confusion matrix plot to {plot_path}")

def plot_roc_curves(roc_curves_data):
    plt.figure(figsize=(8, 6))
    
    for name, (fpr, tpr, auc) in roc_curves_data.items():
        label_name = name.upper().replace('_', ' ')
        plt.plot(fpr, tpr, label=f"{label_name} (AUC = {auc:.4f})", 
                 color=COLORS[name], linewidth=2.5 if name != "baseline" else 1.5,
                 linestyle="--" if name == "baseline" else "-")
                 
    plt.plot([0, 1], [0, 1], 'k:', alpha=0.5, label="Random Guessing (AUC = 0.5000)")
    
    plt.xlim([-0.01, 1.01])
    plt.ylim([-0.01, 1.01])
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity / Recall)")
    plt.title("ROC Curves Comparison", pad=15)
    plt.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()
    
    plot_path = os.path.join(PLOTS_DIR, "roc_curve_comparison.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved ROC comparison plot to {plot_path}")

def plot_feature_importances(importances_dict, feature_names):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    models = ["random_forest", "xgboost"]

    for i, name in enumerate(models):
        if name not in importances_dict:
            continue
            
        importances = importances_dict[name]
        indices = np.argsort(importances)[::-1]

        top_indices = indices[:15]
        top_importances = importances[top_indices]
        top_features = [feature_names[idx] for idx in top_indices]

        df_imp = pd.DataFrame({
            'Feature': top_features,
            'Importance': top_importances
        })

        colors = [COLORS[name]] * 15
        base_color = COLORS[name]
        
        sns.barplot(
            x='Importance', y='Feature', data=df_imp, 
            ax=axes[i], color=base_color, edgecolor='grey', alpha=0.9
        )
        
        axes[i].set_title(f"Feature Importance - {name.upper().replace('_', ' ')} (Top 15)", pad=15)
        axes[i].set_xlabel("Relative Importance")
        axes[i].set_ylabel("")
        
    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, "feature_importance_comparison.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved feature importance comparison plot to {plot_path}")

if __name__ == "__main__":
    evaluate_models()

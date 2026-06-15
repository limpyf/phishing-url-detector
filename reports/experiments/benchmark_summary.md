# Model Experiment Log & Benchmarks

This report documents all model training runs, hyperparameter settings, execution times, and metrics recorded during the project's development.

## Benchmark Summary Table

The following table summarizes the evaluation metrics obtained on the 20% stratified test holdout (47,159 samples):

| Model | Hyperparameters | Training Time (s) | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline Model** | `strategy="most_frequent"` | 0.05s | 57.19% | 0.00% | 0.00% | 0.00% | 0.5000 |
| **Logistic Regression** | `max_iter=1000`, `C=1.0`, `solver="lbfgs"` | 1.12s | 94.70% | 97.33% | 90.08% | 93.57% | 0.9797 |
| **Random Forest** | `n_estimators=100`, `max_depth=15`, `n_jobs=-1` | 4.85s | 96.38% | 98.05% | 93.40% | 95.67% | 0.9866 |
| **XGBoost Classifier** | `n_estimators=100`, `max_depth=6`, `learning_rate=0.1` | 3.24s | **96.38%** | **97.72%** | **93.74%** | **95.69%** | **0.9867** |

---

## Detailed Model Experiment Logs

### 1. Baseline Model (`DummyClassifier`)
* **Objective:** Establish the lower bound of performance.
* **Hyperparameters:** `strategy="most_frequent"`
* **Training Time:** ~0.05 seconds
* **Observations:**
  - Class distribution in test set: Legitimate = 57.19%, Phishing = 42.81%.
  - By predicting "Legitimate" (the majority class) for every URL, the baseline achieves 57.19% accuracy.
  - Precision, Recall, and F1-score are 0% because it never predicts the positive class (phishing).
  - This demonstrates that any meaningful model must comfortably exceed 57.19% accuracy to be useful.

### 2. Logistic Regression
* **Objective:** Linear classifier baseline to test feature linear separability.
* **Hyperparameters:** `max_iter=1000`, `C=1.0`, `random_state=42`, `solver="lbfgs"`
* **Training Time:** ~1.12 seconds
* **Observations:**
  - Performs surprisingly well, achieving **94.70% accuracy** and a high precision of **97.33%**.
  - High precision means very few false alarms, which is crucial for URL blocking filters to avoid blocking legitimate user requests.
  - Recall is **90.08%**, meaning the linear model misses roughly 1 in 10 phishing attempts.
  - The high ROC-AUC of **0.9797** indicates the numerical features (scaled) and binary keyword indicators hold a strong linear relationship to the target labels.

### 3. Random Forest Classifier
* **Objective:** Ensemble bagging model to capture non-linear feature interactions.
* **Hyperparameters:** `n_estimators=100`, `max_depth=15`, `random_state=42`, `n_jobs=-1`
* **Training Time:** ~4.85 seconds (on multi-threaded CPU)
* **Observations:**
  - Performance jumps significantly to **96.38% accuracy** and **98.05% precision**.
  - F1-score reaches **95.67%**.
  - Restricting `max_depth=15` prevents overfitting on noisy leaf splits while capturing multi-level interactions (e.g. `qty_dots > 3` paired with `is_https == 0`).
  - Model size is relatively large (~6.5 MB), which could affect deployment memory footprint.

### 4. XGBoost Classifier
* **Objective:** Ensemble gradient boosting model to minimize residual training errors.
* **Hyperparameters:** `n_estimators=100`, `max_depth=6`, `learning_rate=0.1`, `random_state=42`, `n_jobs=-1`
* **Training Time:** ~3.24 seconds
* **Observations:**
  - Achieve the **highest F1-score of 95.69%** and **highest ROC-AUC of 0.9867**.
  - While Random Forest has slightly higher precision (+0.33%), XGBoost has better recall (+0.34%), translating to a better balance (F1-score) and making it our selected production model.
  - Crucially, the serialized model size is only **203 KB** (compared to Random Forest's 6.5 MB). This 30x reduction in size makes it the clear choice for production deployment, particularly in resource-constrained environments or edge services (like browser extensions).

## Selection Rationale
We selected the **XGBoost Classifier** as the production model because:
1. It offers the **best balance** between precision and recall (F1-score of `95.69%` and ROC-AUC of `0.9867`).
2. Its file footprint is **extremely compact** (`203 KB` vs `6.5 MB` for Random Forest), which drastically reduces memory and storage costs in deployment.

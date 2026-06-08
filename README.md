# Machine Learning Based Phishing URL Detection

---

## Project Overview
This project presents an academic, university-grade machine learning system designed to detect **Phishing URLs** by analyzing their lexical, structural, and behavioral features. 


### Team Members
* **Maksim Koval** mkoval@edu.cdv.pl
* **Denys Burka** dburka@edu.cdv.pl

---

## Motivation
Phishing constitutes one of the most prevalent cyber threats worldwide, wherein deceptive URLs are employed by attackers to mimic trusted brands and extract user credentials. The ineffectiveness of traditional detection systems against newly registered domains stems from their reliance on static blacklists.

Machine learning provides a dynamic alternative through its capacity to identify structural anomalies, suspicious patterns, urgency-inducing keywords, and other distinctive features of phishing URLs, thereby facilitating real-time detection of previously unknown malicious websites.

---

## Dataset
This project utilizes the **PhiUSIIL Phishing URL Dataset** from the UCI Machine Learning Repository. 
* **Total Samples:** 235,795 URLs
* **Class Balance:** 134,850 Legitimate URLs (57.19%) vs. 100,945 Phishing URLs (42.81%)


---

## Features

Soon

---

## Models
We train and compare four models:
1. **Baseline Model** (`DummyClassifier`)
2. **Logistic Regression**
3. **Random Forest Classifier**
4. **XGBoost Classifier**

---

## Results

Soon

---

## Visualizations

Soon

---

## Installation
1. Clone the repository or navigate to the directory.
   ```
   git clone git@github.com:limpyf/phishing-url-detector.git
   cd phishing-url-detector
   ```
2. Create and activate a virtual environment:
   ```powershell
   py -m venv venv
   .\venv\Scripts\activate
   ```
3. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Place the dataset `PhiUSIIL_Phishing_URL_Dataset.csv` inside the `data/raw/` directory.

---

## Usage

### Full Pipeline Training
To preprocess the dataset, train all four models, compare their ROC-AUC scores, and automatically select the best model:
```powershell
python main.py --train
```

### Re-Evaluation
To load existing models and regenerate evaluation metrics and plots without retraining:
```powershell
python main.py --evaluate
```

### Live URL Prediction
To run a live prediction on a URL using the auto-selected best model:
```powershell
python main.py --predict "https://paypal-security-login.com"
```

**Output Example:**


Soon

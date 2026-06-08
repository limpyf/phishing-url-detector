# Machine Learning Based Phishing URL Detection
---

## Project Overview
This project presents an academic, university-grade machine learning system designed to detect **Phishing URLs** by analyzing their lexical, structural, and behavioral features. 

### Team Members
* **Maksim Koval** (mkoval@edu.cdv.pl)
* **Denys Burka** (dburka@edu.cdv.pl)

---

## Motivation
Phishing constitutes one of the most prevalent cyber threats worldwide, wherein deceptive URLs are employed by attackers to mimic trusted brands and extract user credentials. The ineffectiveness of traditional detection systems against newly registered domains stems from their reliance on static blacklists.

Machine learning provides a dynamic alternative through its capacity to identify structural anomalies, suspicious patterns, urgency-inducing keywords, and other distinctive features of phishing URLs, thereby facilitating real-time detection of previously unknown malicious websites.

---

## Dataset
This project utilizes the **PhiUSIIL Phishing URL Dataset** from the UCI Machine Learning Repository 
* **Total Samples:** 235,795 URLs
* **Class Balance:** 134,850 Legitimate URLs (57.19%) vs. 100,945 Phishing URLs (42.81%)

---

## Features

| Feature Name          | Type      |
|----------------------|-----------|
| `url_length`         | Numerical |
| `qty_digits`         | Numerical |
| `qty_dots`           | Numerical |
| `qty_hyphens`        | Numerical |
| `is_https`           | Binary    |
| `is_ip`              | Binary    |
| `qty_subdomains`     | Numerical |
| `qty_special_chars`  | Numerical |
| `keyword_login`      | Binary    |
| `keyword_verify`     | Binary    |
| `keyword_secure`     | Binary    |
| `keyword_update`     | Binary    |
| `keyword_account`    | Binary    |
| `keyword_password`   | Binary    |
| `keyword_banking`    | Binary    |
| `keyword_confirm`    | Binary    |


---

## Models
We train and compare four models:
1. **Baseline Model** (`DummyClassifier`)
2. **Logistic Regression**
3. **Random Forest Classifier**
4. **XGBoost Classifier**

---

## Results

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline Model** | 57.19% | 0.00% | 0.00% | 0.00% | 0.5000 |
| **Logistic Regression** | 94.70% | 97.33% | 90.08% | 93.57% | 0.9797 |
| **Random Forest** | 96.38% | 98.05% | 93.40% | 95.67% | 0.9866 |
| **XGBoost Classifier** | **96.38%** | **97.72%** | **93.74%** | **95.69%** | **0.9867** |

---

## Visualizations

### Class Distribution
![Class Distribution](assets/plots/class_distribution.png)

### ROC Curves Comparison
![ROC Curve](assets/plots/roc_curve_comparison.png)

### Feature Importance (Random Forest vs. XGBoost)
![Feature Importance](assets/plots/feature_importance_comparison.png)

### Confusion Matrices
| Baseline | Logistic Regression |
| :---: | :---: |
| ![CM Baseline](assets/plots/confusion_matrix_baseline.png) | ![CM Logistic](assets/plots/confusion_matrix_logistic_regression.png) |

| Random Forest | XGBoost |
| :---: | :---: |
| ![CM Random Forest](assets/plots/confusion_matrix_random_forest.png) | ![CM XGBoost](assets/plots/confusion_matrix_xgboost.png) |

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
```powershell
python main.py --train
```

### Re-Evaluation

```powershell
python main.py --evaluate
```

### Live URL Prediction

```powershell
python main.py --predict "https://paypal-security-login.com"
```

**Output Example:**
```text
============================================================
PHISHING URL DETECTOR - ANALYSIS
============================================================
Target URL: https://paypal-security-login.com

Prediction: PHISHING

Confidence: 99.9%

Detected indicators:
 ✓ contains_login
 ✓ multiple_hyphens (2 hyphens)
============================================================
```

***

# System Wykrywania Phishingowych Adresów URL Oparty na Uczeniu Maszynowym

---

## Opis Projektu

Projekt przedstawia akademicki system wykrywania **phishingowych adresów URL** oparty na metodach uczenia maszynowego. System analizuje cechy leksykalne, strukturalne oraz behawioralne adresów URL w celu identyfikacji potencjalnych zagrożeń.

### Autorzy

* **Maksim Koval** ([mkoval@edu.cdv.pl](mailto:mkoval@edu.cdv.pl))
* **Denys Burka** ([dburka@edu.cdv.pl](mailto:dburka@edu.cdv.pl))

---

## Motywacja

Phishing jest jednym z najpowszechniejszych zagrożeń cybernetycznych na świecie. Atakujący wykorzystują fałszywe adresy URL imitujące zaufane marki i serwisy internetowe w celu wyłudzenia danych uwierzytelniających użytkowników.

Tradycyjne systemy wykrywania zagrożeń, oparte głównie na statycznych czarnych listach, często okazują się nieskuteczne wobec nowo zarejestrowanych domen phishingowych. Uczenie maszynowe stanowi dynamiczną alternatywę, umożliwiając wykrywanie anomalii strukturalnych, podejrzanych wzorców, słów kluczowych wywołujących poczucie pilności oraz innych charakterystycznych cech adresów URL wykorzystywanych w atakach phishingowych.

Dzięki temu możliwe jest wykrywanie wcześniej nieznanych złośliwych stron internetowych w czasie rzeczywistym.

---

## Zbiór Danych

Projekt wykorzystuje **PhiUSIIL Phishing URL Dataset** pochodzący z repozytorium UCI Machine Learning Repository.

* **Łączna liczba próbek:** 235 795 adresów URL
* **Rozkład klas:** 134 850 legalnych adresów URL (57,19%) oraz 100 945 phishingowych adresów URL (42,81%)

---

## Cechy (Features)

| Nazwa cechy         | Typ        |
| ------------------- | ---------- |
| `url_length`        | Numeryczna |
| `qty_digits`        | Numeryczna |
| `qty_dots`          | Numeryczna |
| `qty_hyphens`       | Numeryczna |
| `is_https`          | Binarna    |
| `is_ip`             | Binarna    |
| `qty_subdomains`    | Numeryczna |
| `qty_special_chars` | Numeryczna |
| `keyword_login`     | Binarna    |
| `keyword_verify`    | Binarna    |
| `keyword_secure`    | Binarna    |
| `keyword_update`    | Binarna    |
| `keyword_account`   | Binarna    |
| `keyword_password`  | Binarna    |
| `keyword_banking`   | Binarna    |
| `keyword_confirm`   | Binarna    |

---

## Modele

W projekcie trenowane i porównywane są cztery modele:

1. **Model Bazowy** (`DummyClassifier`)
2. **Regresja Logistyczna**
3. **Las Losowy (Random Forest Classifier)**
4. **XGBoost Classifier**

---

## Wyniki

| Model                    |  Accuracy  |  Precision |   Recall   |  F1 Score  |   ROC-AUC  |
| :----------------------- | :--------: | :--------: | :--------: | :--------: | :--------: |
| **Model Bazowy**         |   57.19%   |    0.00%   |    0.00%   |    0.00%   |   0.5000   |
| **Regresja Logistyczna** |   94.70%   |   97.33%   |   90.08%   |   93.57%   |   0.9797   |
| **Random Forest**        |   96.38%   |   98.05%   |   93.40%   |   95.67%   |   0.9866   |
| **XGBoost Classifier**   | **96.38%** | **97.72%** | **93.74%** | **95.69%** | **0.9867** |

---

## Wizualizacje

### Rozkład Klas

![Class Distribution](assets/plots/class_distribution.png)

### Porównanie Krzywych ROC

![ROC Curve](assets/plots/roc_curve_comparison.png)

### Ważność Cech (Random Forest vs. XGBoost)

![Feature Importance](assets/plots/feature_importance_comparison.png)

### Macierze Pomyłek (Confusion Matrices)

|                        Model Bazowy                        |                          Regresja Logistyczna                         |
| :--------------------------------------------------------: | :-------------------------------------------------------------------: |
| ![CM Baseline](assets/plots/confusion_matrix_baseline.png) | ![CM Logistic](assets/plots/confusion_matrix_logistic_regression.png) |

|                             Random Forest                            |                          XGBoost                         |
| :------------------------------------------------------------------: | :------------------------------------------------------: |
| ![CM Random Forest](assets/plots/confusion_matrix_random_forest.png) | ![CM XGBoost](assets/plots/confusion_matrix_xgboost.png) |

---

## Instalacja

1. Sklonuj repozytorium i przejdź do katalogu projektu:

```bash
git clone git@github.com:limpyf/phishing-url-detector.git
cd phishing-url-detector
```

2. Utwórz i aktywuj środowisko wirtualne:

```powershell
py -m venv venv
.\venv\Scripts\activate
```

3. Zainstaluj wymagane zależności:

```powershell
pip install -r requirements.txt
```

4. Umieść plik `PhiUSIIL_Phishing_URL_Dataset.csv` w katalogu `data/raw/`.

---

## Użytkowanie

### Trenowanie Pełnego Pipeline'u

```powershell
python main.py --train
```

### Ponowna Ewaluacja Modeli

```powershell
python main.py --evaluate
```

### Analiza Adresu URL w Czasie Rzeczywistym

```powershell
python main.py --predict "https://paypal-security-login.com"
```

### Przykładowy Wynik

```text
============================================================
DETEKTOR PHISHINGOWYCH ADRESÓW URL - ANALIZA
============================================================
Analizowany adres URL:
https://paypal-security-login.com

Wynik klasyfikacji:
PHISHING

Poziom pewności:
99.9%

Wykryte wskaźniki:
 ✓ contains_login
 ✓ multiple_hyphens (2 myślniki)
============================================================
```

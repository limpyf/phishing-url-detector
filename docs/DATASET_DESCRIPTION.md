# Dataset Description - PhiUSIIL Phishing URL Dataset

This document provides details on the dataset used for training and evaluating the Phishing URL Detector.

## Dataset Overview

The dataset used is the **PhiUSIIL Phishing URL Dataset**, obtained from the UCI Machine Learning Repository. It contains lexical, structural, and behavioral features of phishing and legitimate URLs.

* **Total Samples:** 235,795 URLs
* **Legitimate Class (0):** 134,850 samples (57.19%)
* **Phishing Class (1):** 100,945 samples (42.81%)
* **Class Balance:** Relatively balanced (no extreme class imbalance, making F1-score and ROC-AUC highly representative metrics).

## Source Reference

* **Repository:** UCI Machine Learning Repository
* **Dataset Link:** [UCI PhiUSIIL Phishing URL Dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)
* **Citation:** Prasad, A., & Chandra, S. (2023). PhiUSIIL Phishing URL Dataset. UCI Machine Learning Repository.

## Target Label Alignment

> [!IMPORTANT]
> In the original UCI dataset, the `label` column encodes **1 for Legitimate** and **0 for Phishing**. 
> To align with standard ML conventions where the positive class represents the anomaly/threat, our preprocessing pipeline **inverts the label** (`1 - label`).
>
> In this repository:
> * `1` represents **Phishing** (Malicious)
> * `0` represents **Legitimate** (Safe)

## Extracted Handcrafted Features

While the raw dataset contains 54 columns (including complex web page content features, PageRank, WHOIS domain age, etc.), this project focuses on **pure lexical and structural analysis** of the URL string itself. This allows for instant predictions without sending requests to live sites (preserving user privacy and preventing execution of malicious payloads).

We extract **16 core features** grouped into three categories:

### 1. Length & Lexical Features
* `url_length` (Numerical): Total character length of the URL.
* `qty_digits` (Numerical): Count of numeric digits `[0-9]` in the URL.
* `qty_special_chars` (Numerical): Count of suspicious characters: `@`, `?`, `=`, `&`, and `%`.

### 2. Structural Features
* `qty_dots` (Numerical): Count of dots `.` (used to identify subdomain spamming).
* `qty_hyphens` (Numerical): Count of hyphens `-` (often used to mimic legitimate names).
* `qty_subdomains` (Numerical): Number of subdomains detected in the hostname.
* `is_https` (Binary): `1` if the URL protocol starts with `https`, `0` otherwise.
* `is_ip` (Binary): `1` if the host portion is a raw IPv4/IPv6 address, `0` otherwise.

### 3. Suspicious Keyword Indicators (Binary)
We check for the presence (case-insensitive) of common phishing keywords:
* `keyword_login`: presence of "login"
* `keyword_verify`: presence of "verify"
* `keyword_secure`: presence of "secure"
* `keyword_update`: presence of "update"
* `keyword_account`: presence of "account"
* `keyword_password`: presence of "password"
* `keyword_banking`: presence of "banking"
* `keyword_confirm`: presence of "confirm"

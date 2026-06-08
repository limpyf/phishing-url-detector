import re
from urllib.parse import urlparse
import pandas as pd

def is_valid_ip(host):
    ipv4_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(ipv4_pattern, host):
        parts = host.split('.')
        return all(0 <= int(part) <= 255 for part in parts)

    ipv6_pattern = r"^\[?[0-9a-fA-F:]+\]?$"
    if ":" in host and re.match(ipv6_pattern, host):
        return True
    
    return False

def extract_features_from_url(url):
    if not isinstance(url, str):
        url = ""
    
    url_lower = url.lower()

    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        parsed_url = urlparse("http://" + url)
    
    host = parsed_url.hostname or ""

    url_length = len(url)

    qty_digits = sum(c.isdigit() for c in url)

    qty_dots = url.count('.')

    qty_hyphens = url.count('-')

    is_https = 1 if url_lower.startswith("https") else 0

    is_ip = 1 if is_valid_ip(host) else 0

    host_parts = host.split('.')

    if len(host_parts) > 2:
        qty_subdomains = len(host_parts) - 2
    else:
        qty_subdomains = 0

    keywords = ['login', 'verify', 'secure', 'update', 'account', 'password', 'banking', 'confirm']
    keyword_features = {}
    for kw in keywords:
        keyword_features[f"keyword_{kw}"] = 1 if kw in url_lower else 0

    qty_special_chars = sum(url.count(char) for char in ['@', '?', '=', '&', '%'])

    features = {
        'url_length': url_length,
        'qty_digits': qty_digits,
        'qty_dots': qty_dots,
        'qty_hyphens': qty_hyphens,
        'is_https': is_https,
        'is_ip': is_ip,
        'qty_subdomains': qty_subdomains,
        'qty_special_chars': qty_special_chars
    }

    features.update(keyword_features)
    
    return features

def batch_extract_features(urls_list):
    feature_list = []
    for url in urls_list:
        feature_list.append(extract_features_from_url(url))
    return pd.DataFrame(feature_list)

if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login.php",
        "https://paypal-security-login-update.com/verify-account?user=test",
        "secure.paypal.verify.account.com"
    ]
    
    print("Extracting features for test URLs:")
    for url in test_urls:
        print(f"\nURL: {url}")
        feats = extract_features_from_url(url)
        for k, v in feats.items():
            print(f"  {k}: {v}")

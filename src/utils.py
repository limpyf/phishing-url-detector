import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
PLOTS_DIR = os.path.join(ASSETS_DIR, "plots")
SCREENSHOTS_DIR = os.path.join(ASSETS_DIR, "screenshots")

LOCAL_RAW_PATH = os.path.join(RAW_DATA_DIR, "PhiUSIIL_Phishing_URL_Dataset.csv")

def setup_directories():
    dirs = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        MODELS_DIR,
        PLOTS_DIR,
        SCREENSHOTS_DIR
    ]

    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created directory: {d}")

import os

import xgboost

#configurations for tickers/dates
TICKER = "NBIS"
START_DATE= "2024-01-01"
END_DATE = "2026-05-10"
AVSTART_DATE = START_DATE.replace("-","") + "T0000"
AVEND_DATE = END_DATE.replace("-","") + "T0000"
THRESHOLD = 0.4
c = 0.1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
xgb_model = xgboost.XGBClassifier()
xgb_model.load_model(os.path.join(BASE_DIR, 'models','xgb_model.json'))
feature_cols = xgb_model.get_booster().feature_names

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
MODEL_TRAIN_DIR = os.path.join(BASE_DIR, "data", "model_training")

def processed_path(filename:str) -> str:
    return os.path.join(PROCESSED_DIR, filename)

def model_training_path(filename:str) -> str:
    return os.path.join(MODEL_TRAIN_DIR, filename)

def raw_path(filename:str) -> str:
    return os.path.join(RAW_DIR, filename)
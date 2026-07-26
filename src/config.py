import os

#configurations for tickers/dates
TICKER = "NBIS"
START_DATE= "2024-01-01"
END_DATE = "2026-05-10"
AVSTART_DATE = START_DATE.replace("-","") + "T0000"
AVEND_DATE = END_DATE.replace("-","") + "T0000"
THRESHOLD = 0.4
c = 0.1

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

def processed_path(filename):
    return os.path.join(PROCESSED_DIR, filename)

def raw_path(filename):
    return os.path.join(RAW_DIR, filename)
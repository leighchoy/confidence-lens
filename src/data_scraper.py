from datetime import datetime
from dotenv import load_dotenv

import pandas as pd
import finnhub as fh
import yfinance as yf
import os
import time


from config import *

load_dotenv()
client = fh.Client(api_key=os.getenv('FINNHUB_API_KEY'))


data = client.quote(
    symbol=TICKER
)
finndf = pd.DataFrame([data])




"""history = yf.download(
    tickers="NBIS",
            interval = "5d",
            start = "2025-01-01",
            end = datetime.today().strftime("%Y-%m-%d")
                      )
                      
    ticker = input("Enter ticker symbol: ").upper()
    intv = input("Enter interval (Valid interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo): ")
    st = input("Enter start date (YYYY-MM-DD): ")
    e = input("Enter end date (YYYY-MM-DD): ")
    
"""

def get_history():

    interval = "1d"


    try:
        history = yf.download(TICKER, interval = interval, start = START_DATE, end = END_DATE,prepost=True)
        price_df = pd.DataFrame.from_dict(history)
        price_df.columns = price_df.columns.get_level_values(0)

        if history.empty:
            print("No data found for this ticker or timeframe.")
            return None
        return price_df

    except Exception as e:
        print(f"Error: {e}")
        return None



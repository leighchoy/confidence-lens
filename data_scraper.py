from datetime import datetime
from dotenv import load_dotenv

import pandas as pd
import finnhub as fh
import yfinance as yf
import os
import time

load_dotenv()
client = fh.Client(api_key=os.getenv('FINNHUB_API_KEY'))


data = client.quote(
    symbol="NBIS"
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

def get_history(tickers, interval, start, end):
    ticker = "EONR"
    interval = "5d"
    start = "2025-01-01"
    end = "2026-03-12"

    try:
        history = yf.download(ticker, interval = interval, start = start, end = end,prepost=True)

        if history.empty:
            print("No data found for this ticker or timeframe.")
            return None
        return history

    except Exception as e:
        print(f"Error: {e}")
        return None

    return history

tickers = ""
interval = ""
start = ""
end = ""
history = get_history(tickers, interval, start, end)

print(history)


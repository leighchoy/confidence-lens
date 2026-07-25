from dotenv import load_dotenv

import requests
import pandas as pd
import finnhub as fh
import yfinance as yf
import os

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


def get_income_statement():

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=INCOME_STATEMENT"
        f"&symbol={TICKER}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"

    )
    r = requests.get(url)
    data = r.json()
    articles = data.get("annualReports", [])
    records = []
    for article in articles:
        records.append({
            "fiscal_date": article["fiscalDateEnding"],
            "ebitda": article["ebitda"],
            "net_income": article["netIncome"],
            "revenue": article["totalRevenue"],
            "operating_income": article["operatingIncome"],
            "operating_outcome": article["operatingExpenses"],
            "gross_profit": article["grossProfit"],
            "income_tax_expense": article["incomeTaxExpense"],
        })
    return pd.DataFrame(records)

def get_cash_flow():
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=CASH_FLOW"
        f"&symbol={TICKER}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
    r = requests.get(url)
    data = r.json()
    articles = data.get("annualReports", [])
    records = []
    for article in articles:
        records.append({
            "fiscal_date": article["fiscalDateEnding"],
            "operating_cash_flow": article["operatingCashflow"],
            "capital_expenditure": article["capitalExpenditures"],
            "free_cash_flow": article["operatingCashFlow"] - article["capitalExpenditures"],
            "depreciation": article["depreciationDepletionAndAmortization"]
        })

def get_balance_sheet():
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=BALANCE_SHEET"
        f"&symbol={TICKER}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
    r = requests.get(url)
    data = r.json()
    articles = data.get("annualReports", [])
    records = []
    print(url)
    for article in articles:
        records.append({
            "fiscal_date": article["fiscalDateEnding"],
            "current_assets": article["totalCurrentAssets"],
            "total_debt": article["shortTermDebt"] + article["longTermDebt"],
            "current_liabilities": article["totalCurrentLiabilities"],
            "outstanding_shares": article["commonStockSharesOutstanding"]
        })

def get_earnings_call():
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=EARNINGS"
        f"&symbol={TICKER}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
    r = requests.get(url)
    data = r.json()
    articles = data.get("annualEarnings", [])
    records = []
    print(url)
    for article in  articles:
        records.append({
            "fiscal_date": article["fiscalDateEnding"],
            "EPS": article["reportedEPS"],
        })
    articles = data.get("quarterlyEarnings", [])
    for article in articles:
        records.append({
            "fiscal_date": article["fiscalDateEnding"],
            "reported_EPS": article["reportedEPS"],
            "estimated_EPS": article["estimatedEPS"],
            "released_date": article["reportedDate"],
            "surprise":article["surprise"],

        })

def get_earnings_estimates():
    url =(
        f"https://www.alphavantage.co/query"
        f"?function=EARNINGS_ESTIMATES"
        f"&symbol={TICKER}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"

    )
    r = requests.get(url)
    data = r.json()

    articles = data.get("estimates", [])
    records = []

    for article in articles:
        records.append({
            "date": article["date"],
            "horizon": article["horizon"],
            "estimated_EPS": article["eps_estimate_average"],
            "estimated_revenue": article["revenue_estimate_average"],
        })


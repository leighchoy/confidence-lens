from dotenv import load_dotenv

import requests
import pandas as pd
import yfinance as yf
import os


load_dotenv()

"""
Function to handle null values and convert strings to floats
"""

def clean_data(input):
    try:
        if input == None or input == "" or input == "None":
            return 0
        return float(input)
    except Exception as e:
        print("Error cleaning company fundamental series")

def get_history(ticker,start_date,end_date):

    interval = "1d"


    try:
        history = yf.download(ticker, interval = interval, start = start_date, end = end_date,prepost=True)
        price_df = pd.DataFrame.from_dict(history)
        price_df.columns = price_df.columns.get_level_values(0)

        if history.empty:
            print("No data found for this ticker or timeframe.")
            return None
        return price_df

    except Exception as e:
        print(f"Error retrieving stock price history: {e}")


def get_income_statement(ticker)->pd.DataFrame:

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=INCOME_STATEMENT"
        f"&symbol={ticker}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"

    )
    try:
        r = requests.get(url)
        data = r.json()
        articles = data.get("annualReports", [])
        records = []

        for article in articles:
            records.append({
                "fiscal_date": article.get("fiscalDateEnding"),
                "ebitda": clean_data(article.get("ebitda")),
                "net_income": clean_data(article.get("netIncome")),
                "revenue": clean_data(article.get("totalRevenue")),
                "operating_income": clean_data(article.get("operatingIncome")),
                "operating_outcome": clean_data(article.get("operatingExpenses")),
                "gross_profit": clean_data(article.get("grossProfit")),
                "income_tax_expense": clean_data(article.get("incomeTaxExpense")),
                "interest_expense": clean_data(article.get("interestExpense"))
            })
        return pd.DataFrame(records)
    except Exception as e:
        print(f"Error retrieving income statement: {e}")
        return pd.DataFrame()

def get_cash_flow(ticker)->pd.DataFrame:
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=CASH_FLOW"
        f"&symbol={ticker}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
    try:
        r = requests.get(url)
        data = r.json()
        articles = data.get("annualReports", [])
        records = []
        for article in articles:
            records.append({
                "fiscal_date": article.get("fiscalDateEnding"),
                "operating_cash_flow": clean_data(article.get("operatingCashflow")),
                "capital_expenditure": clean_data(article.get("capitalExpenditures")),
                "free_cash_flow": clean_data(article.get("operatingCashflow")) - clean_data(article.get("capitalExpenditures")),
                "depreciation": clean_data(article.get("depreciationDepletionAndAmortization"))
            })

        return pd.DataFrame(records)
    except Exception as e:
        print(f"Error retrieving cash flow statement: {e}")
        return pd.DataFrame()

def get_balance_sheet(ticker)->pd.DataFrame:
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=BALANCE_SHEET"
        f"&symbol={ticker}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
    r = requests.get(url)
    try:
        data = r.json()
        articles = data.get("annualReports", [])
        records = []

        for article in articles:
            records.append({
                "fiscal_date": article["fiscalDateEnding"],
                "current_assets": clean_data(article.get("totalCurrentAssets")),
                "total_debt": clean_data(article.get("shortTermDebt") or 0) + (clean_data(article.get("longTermDebt")) or 0),
                "current_liabilities": clean_data(article.get("totalCurrentLiabilities")),
                "outstanding_shares": clean_data(article.get("commonStockSharesOutstanding"))
            })
        records = pd.DataFrame(records)
        return records
    except Exception as e:
        print(f"Error retrieving balance sheet: {e}")
        return pd.DataFrame()

def get_earnings_call(ticker)->tuple[pd.DataFrame,pd.DataFrame]:
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=EARNINGS"
        f"&symbol={ticker}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
    try:
        r = requests.get(url)
        data = r.json()
        articles = data.get("annualEarnings", [])
        yearly_records = []

        for article in  articles:
            yearly_records.append({
                "fiscal_date": article.get("fiscalDateEnding"),
                "EPS": article.get("reportedEPS"),
            })
        articles = data.get("quarterlyEarnings", [])
        quarterly_records = []
        for article in articles:
            quarterly_records.append({
                "fiscal_date": article.get("fiscalDateEnding"),
                "reported_EPS": clean_data(article.get("reportedEPS")),
                "estimated_EPS": clean_data(article.get("estimatedEPS")),
                "released_date": clean_data(article.get("reportedDate")),
                "surprise":clean_data(article.get("surprise"))

            })
        quarterly_records = pd.DataFrame(quarterly_records)
        yearly_records = pd.DataFrame(yearly_records)
        return quarterly_records, yearly_records
    except Exception as e:
        print(f"Error retrieving quarterly and yearly earnings calls: {e}")
        return pd.DataFrame(),pd.DataFrame()


def get_earnings_estimates(ticker)->pd.DataFrame:
    url =(
        f"https://www.alphavantage.co/query"
        f"?function=EARNINGS_ESTIMATES"
        f"&symbol={ticker}"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"

    )
    try:
        r = requests.get(url)
        data = r.json()

        articles = data.get("estimates", [])
        records = []


        for article in articles:
            records.append({
                "date": article.get("date"),
                "horizon": clean_data(article.get("horizon")),
                "estimated_EPS": clean_data(article.get("eps_estimate_average")),
                "estimated_revenue": clean_data(article.get("revenue_estimate_average"))
            })
        records = pd.DataFrame(records)
        return records
    except Exception as e:
        print(f"Error retrieving earnings estimates: {e}")
        return pd.DataFrame()


def get_company_overview(ticker)->pd.DataFrame:
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=OVERVIEW"
        f"&symbol={ticker}"
        f"&apikey={os.getenv("ALPHAV_API_KEY")}"

    )
    try:
        r = requests.get(url)
        data = r.json()
        records = {
            "latest_quarter": data.get("LatestQuarter"),
            "P/E": data.get("PERatio"),
            "EPS": data.get("EPS"),
            "Beta": data.get("Beta"),
            "Description": data.get("Description"),
            "Sector": data.get("Sector"),
            "Industry": data.get("Industry"),
            "Name": data.get("Name")
       }
        records = pd.DataFrame([records])
        return records
    except Exception as e:
        print(f"Error retrieving company overview: {e}")
        return pd.DataFrame()

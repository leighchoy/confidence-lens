
from data_modifier import *
from feature_engineering import tech_analysis
from data_scraper import *
from language_model import *
import time

ticker = "NBIS"
start_date = "2025-01-01"
end_date = "2026-05-10"
price_df = get_history(ticker, start_date, end_date)
print("price_df",price_df.head())
price_df = clean_history(price_df)
print("cleaned")
tech_analysis_df = tech_analysis(price_df)
print("tech_analysis_df",tech_analysis_df.head())

prediction, probability = get_prediction(xgb_model, tech_analysis_df)
print("prediction",prediction,"probability",probability)
balance_df = get_balance_sheet(ticker)
time.sleep(1.1)
income_df = get_income_statement(ticker)
time.sleep(1.1)
cash_df = get_cash_flow(ticker)
time.sleep(1.1)
company_overview = get_company_overview(ticker)

print(balance_df.columns.tolist())
print(income_df.columns.tolist())
print(cash_df.columns.tolist())
print(company_overview.columns.tolist())

financials, dcf = calculate_all(balance_df, price_df, income_df, cash_df, company_overview)
print("financials",financials.head(),"dcf",dcf.head())
thesis = get_lm_thesis(ticker, financials, dcf, results_df, company_overview)



from data_modifier import clean_history
from feature_engineering import tech_analysis
from signal_model import get_prediction
from language_model import get_lm_thesis
from config import processed_path, model_training_path, xgb_model, feature_cols
from fundamental_calculations import calculate_all
from data_scraper import get_balance_sheet,get_income_statement,get_company_overview,get_cash_flow,get_history
import pandas as pd
import time

results_df = pd.DataFrame(pd.read_csv(model_training_path("trimmed_class_report_xgb.csv")))
"""balance_df = pd.DataFrame(pd.read_csv(processed_path("balance_sheet.csv")))
income_df = pd.DataFrame(pd.read_csv(processed_path("income_statement.csv")))
cash_df = pd.DataFrame(pd.read_csv(processed_path("cash_flow.csv")))
company_overview = pd.DataFrame(pd.read_csv(processed_path("company_overview.csv")))
price_df = pd.DataFrame(pd.read_csv(processed_path("price_df.csv")))
"""
ticker = "NBIS"
start_date = "2025-01-01"
end_date = "2026-05-10"
price_df = get_history(ticker, start_date, end_date)
price_df = clean_history(price_df)
tech_analysis_df = tech_analysis(price_df)

prediction, probability = get_prediction(xgb_model,feature_cols,tech_analysis_df)

balance_df = get_balance_sheet(ticker)
time.sleep(1.1)
income_df = get_income_statement(ticker)
time.sleep(1.1)
cash_df = get_cash_flow(ticker)
time.sleep(1.1)
company_overview = get_company_overview(ticker)

financials, dcf = calculate_all(balance_df, price_df, income_df, cash_df, company_overview)
thesis = get_lm_thesis(ticker, financials, dcf, results_df, company_overview)
#raise DataSourceError(...) from e
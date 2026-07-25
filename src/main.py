from src.news_scraper import get_company_news
from src.data_modifier import *
from src.data_scraper import get_history
from src.feature_engineering import tech_analysis
from src.signal_model import *
import pandas as pd
import os

#build price dataframe
price_df = get_history()

#build headline dataframe
news_df = get_company_news()


#save raw data
news_df.to_csv("../data/raw/news_df.csv", index=False)

price_df.to_csv("../data/raw/price_df.csv", index=True)

#clean data
price_df = clean_history(price_df)
price_df.to_csv("../data/processed/price_df.csv", index=True)

#clean and add sentiment and confidence
news_df = clean_news(news_df)

news_df.to_csv("../data/processed/news_df.csv", index=True)


merged_df = merge_data(price_df, news_df)
merged_df.to_csv("../data/processed/merged_data.csv", index=True)


news_df = tech_analysis(merged_df)
news_df.to_csv("../data/processed/tech_analysis.csv", index =True)

_,_,_,_,_,y_test = prepare_data(df)
results = []
_,y_pred,y_prob=train_model_lr(df)
append_summary_row(results,"Logistic Regression", "3 price features", y_test,y_pred,y_prob)
_,y_pred,y_prob=train_model_rf(df)
append_summary_row(results,"Random Forest Classifier", "6 price features", y_test,y_pred,y_prob)
_,y_pred,y_prob=train_model_xgb(df)
append_summary_row(results,"XGBoost Classifier", "6 price features", y_test,y_pred,y_prob)
results_df = pd.DataFrame(results)
results_df.to_csv("../data/model_training/comparison_report.csv", index=False)

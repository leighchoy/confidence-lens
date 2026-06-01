from src.news_scraper import get_company_news
from src.data_scraper import get_history
import pandas as pd
import os

newsdf = pd.DataFrame.from_dict(get_company_news())
newsdf = newsdf[["headline", "datetime", "summary"]]

newsdf.to_csv("../data/raw/newsdf.csv", index=False)

#chagning time presentation
newsdf["datetime"] = pd.to_datetime(newsdf["datetime"],unit = 's',utc=True)

#need function for changing buckets
newsdf["bucket"] = newsdf["datetime"].dt.floor("5min")

newsdf = add_sentiment(newsdf)
print(newsdf[["headline","sentiment"]].tail(10))
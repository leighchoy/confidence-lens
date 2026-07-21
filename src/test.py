from src.news_scraper import *
from src.data_modifier import *


#news_df = add_sentiment(news_df)
news_df = clean_avnews(news_df)
print(news_df)
news_df.to_csv("../data/raw/test.csv", index=False)

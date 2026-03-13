from dotenv import load_dotenv

import os
import finnhub
import pandas as pd
import vaderSentiment as vs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()
client = finnhub.Client(api_key= os.getenv("FINNHUB_API_KEY"))

#function for getting sentiment score of an individual string
def sentiment_score(text):
    if not isinstance(text, str) or text.strip() == "":
        return 0.0
    sent_dict = sid_obj.polarity_scores(text)
    return sent_dict['compound']

#function to add sentiment to dataframe
def add_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    text = df["headline"]
    df = df.copy()
    df["sentiment"] = text.apply(sentiment_score)
    return df


def get_company_news():
    symbol = input("Enter the company symbol: ")
    sDate = input("Enter the start date (YYYY-MM-DD): ")
    eDate = input("Enter the end date (YYYY-MM-DD): ")
    news = client.company_news(symbol, sDate, eDate)
    return news

newsdf = pd.DataFrame.from_dict(get_company_news())
newsdf = pd.concat([newsdf.iloc[:,5],newsdf.iloc[:,1:3]], axis = 1)

sid_obj = SentimentIntensityAnalyzer()

for x in newsdf.index:
    print(x)
    print(sentiment_score(x))

#add_sentiment(newsdf)
#print(newsdf.tail())







#chagning time presentation
newsdf["datetime"] = pd.to_datetime(newsdf["datetime"],unit = 's',utc=True)

#need function for changing buckets
newsdf["bucket"] = newsdf["datetime"].dt.floor("5min")

#newsdf.sort_values("bucket",ascending = True,inplace = True)

for x in newsdf["headline"]:
    print(x)
    print(sentiment_score(x))



target_sent = newsdf["headline"].iloc[0]
print(target_sent)
#print(sentiment_score(target_sent))

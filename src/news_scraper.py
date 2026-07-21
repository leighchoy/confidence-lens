from dotenv import load_dotenv
from huggingface_hub import login

import os
import finnhub
import requests
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from config import *

load_dotenv()
login(os.getenv("FINBERT_API_KEY"))
client = finnhub.Client(api_key= os.getenv("FINNHUB_API_KEY"))

tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

pipe = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


#function for getting sentiment score of an individual string (headline)
def sentiment_score(text):
    if not isinstance(text, str) or text.strip() == "":
        return {"score": 0.0, "label": "neutral"}
    result = pipe(text[:512])[0]
    score = result["score"]



    return {"score": score, "label": result["label"]}

#choosing to only use headlines for sentiment analysis due to constraint on token limits and accuracy is not the main goal
#function to add sentiment to dataframe
def add_sentiment(news_df: pd.DataFrame) -> pd.DataFrame:
    news_df = news_df.copy()
    text = news_df["summary"].where(news_df["summary"].notna() & news_df["summary"].str.strip().ne(""), news_df["headline"])
    results = text.apply(sentiment_score)
    news_df["confidence"] = results.apply(lambda x: x["score"])
    news_df["sentiment"] = results.apply(lambda x: x["label"])
    return news_df

#function for returning company news


def get_company_news():
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=NEWS_SENTIMENT"
        f"&tickers={TICKER}"
        f"&time_from={AVSTART_DATE}"
        f"&time_to={AVEND_DATE}"
        f"&sort=LATEST"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
    r = requests.get(url)
    data = r.json()
    articles = data.get("feed",[])
    records = []
    for article in articles:
        records.append({
            "headline": article["title"],
            "datetime": article["time_published"],
            "sentiment_avg": article["overall_sentiment_score"],
            "sentiment_label": article["overall_sentiment_label"],
        })
    return pd.DataFrame(records)








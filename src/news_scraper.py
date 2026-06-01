from dotenv import load_dotenv

import os
import finnhub
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

pipe = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

load_dotenv()
client = finnhub.Client(api_key= os.getenv("FINNHUB_API_KEY"))




#function for getting sentiment score of an individual string (headline)
def sentiment_score(text):
    if not isinstance(text, str) or text.strip() == "":
        return {"score": 0.0, "label": "neutral"}
    result = pipe(text[:512])[0]
    score = result["score"]
    if result["label"] == "negative":
        score = -score

    return {"score": score, "label": result["label"]}

#choosing to only use headlines for sentiment analysis due to constraint on token limits and accuracy is not the main goal
#function to add sentiment to dataframe
def add_sentiment(newsdf: pd.DataFrame) -> pd.DataFrame:
    text = newsdf["headline"].apply(sentiment_score)
    newsdf = newsdf.copy()
    newsdf["sentiment"] = text.apply(lambda x: x["score"])
    newsdf["sentiment"] = text.apply(lambda x: x["label"])
    return newsdf


def get_company_news():

    news = client.company_news("NBIS", "2026-04-29", "2026-05-10")
    return news

newsdf = pd.DataFrame.from_dict(get_company_news())
newsdf = newsdf[["headline", "datetime", "summary"]]

newsdf.to_csv("../data/raw/newsdf.csv", index=False)

#chagning time presentation
newsdf["datetime"] = pd.to_datetime(newsdf["datetime"],unit = 's',utc=True)

#need function for changing buckets
newsdf["bucket"] = newsdf["datetime"].dt.floor("5min")

newsdf = add_sentiment(newsdf)
print(newsdf[["headline","sentiment"]].tail(10))
#newsdf.sort_values("bucket",ascending = True,inplace = True)





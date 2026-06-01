from dotenv import load_dotenv

import os
import finnhub
import vaderSentiment as vs
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()
client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

i_sentiment = client.stock_insider_sentiment(
    symbol = "NBIS",
    _from = "2026-01-01",
    to = "2026-01-10"
)

print(i_sentiment)


from src.news_scraper import *
from src.data_modifier import *


#news_df = add_sentiment(news_df)
news_df = get_company_news()
print(news_df["feed"][0])
#news_df = clean_news(news_df)
url = (
        f"https://www.alphavantage.co/query"
        f"?function=NEWS_SENTIMENT"
        f"&tickers={TICKER}"
        #f"&time_from={AVSTART_DATE}"
        #f"&time_to={AVEND_DATE}"
        f"&limit=380"
        #f"&sort=LATEST"
        f"&apikey={os.getenv('ALPHAV_API_KEY')}"
    )
print(url)
#news_df = clean_news(news_df)
news_df.to_csv("../data/raw/test.csv", index=False)

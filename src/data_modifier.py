import pandas as pd

#only removes rows with null headline or datetime, summary doesnt matter

#set index to sort easier and also helps with merging method
def clean_news(avnews_df: pd.DataFrame) -> pd.DataFrame:
    avnews_df = avnews_df.copy()
    avnews_df.dropna(subset=["headline", "datetime"], inplace=True)
    avnews_df.drop_duplicates(subset="headline", inplace=True)
    avnews_df["datetime"] = pd.to_datetime(avnews_df["datetime"], format="%Y%m%dT%H%M%S", utc=True)
    avnews_df["bucket"] = avnews_df["datetime"].dt.floor("1d")
    avnews_df["bucket"] = avnews_df["bucket"].dt.tz_localize(None)
    avnews_df.set_index("bucket", inplace=True)
    avnews_df.sort_index(ascending=True, inplace=True)
    return avnews_df

def clean_history(price_df: pd.DataFrame) -> pd.DataFrame:
    price_df = price_df.copy()
    price_df.dropna(subset=["Open", "Close", "High", "Low"], inplace=True)
    price_df["Volume"] = price_df["Volume"].fillna(0)
    price_df.sort_index(ascending = True, inplace=True)
    return price_df

#cant have multiple news headlines in the same row so decided to aggregate them into their own categories/columns
#need to add scoring system for avg_confidence
def aggregate_news(news_df: pd.DataFrame) -> pd.DataFrame:
    news_df = news_df.groupby("bucket").agg(
        Avg_positive_confidence=("sentiment_avg", lambda x: x[x>0].mean() if (x>0).any() else 0),
        Avg_negative_confidence=("sentiment_avg", lambda x: x[x<0].mean() if (x<0).any() else 0),

        Headline_count=("headline","count"),
        Positive_count=("sentiment_label",lambda x: (x == "positive").sum()),
        Negative_count=("sentiment_label", lambda x: (x=="negative").sum()),
        Neutral_count=("sentiment_label", lambda x: (x=="neutral").sum())).reset_index()
    news_df["Overall_confidence"] = news_df["Avg_positive_confidence"] + news_df["Avg_negative_confidence"]
    aggregated_news = news_df.set_index("bucket")
    return aggregated_news

def merge_data(price_df: pd.DataFrame, news_df: pd.DataFrame) -> pd.DataFrame:
    agg_news = aggregate_news(news_df)
    merged = pd.merge(price_df, agg_news, left_index = True, right_index = True, how="left")
    return merged

import pandas as pd


"""def clean_news(avnews_df: pd.DataFrame) -> pd.DataFrame:
    try:
        avnews_df = avnews_df.copy()
        avnews_df.dropna(subset=["headline", "datetime"], inplace=True)
        avnews_df.drop_duplicates(subset="headline", inplace=True)
        avnews_df["datetime"] = pd.to_datetime(avnews_df["datetime"], format="%Y%m%dT%H%M%S", utc=True)
        avnews_df["bucket"] = avnews_df["datetime"].dt.floor("1d")
        avnews_df["bucket"] = avnews_df["bucket"].dt.tz_localize(None)
        avnews_df.set_index("bucket", inplace=True)
        avnews_df.sort_index(ascending=True, inplace=True)
        return avnews_df
    except Exception as e:
        print(f"Error: {e}")"""

def clean_history(price_df: pd.DataFrame) -> pd.DataFrame:
    try:
        price_df = price_df.copy()
        price_df.dropna(subset=["Open", "Close", "High", "Low"], inplace=True)
        price_df["Volume"] = price_df["Volume"].fillna(0)
        price_df.sort_index(ascending = True, inplace=True)
        return price_df
    except Exception as e:
        print(f"Error: {e}")

"""def aggregate_news(news_df: pd.DataFrame) -> pd.DataFrame:
      try:
        news_df = news_df.groupby("bucket").agg(
            Avg_positive_confidence=("sentiment_avg", lambda x: x[x>0].mean() if (x>0).any() else 0),
            Avg_negative_confidence=("sentiment_avg", lambda x: x[x<0].mean() if (x<0).any() else 0),
            Headline_count=("headline","count"),
            Positive_count=("sentiment_label",lambda x: (x == "Bullish").sum() + (x == "Somewhat-Bullish").sum()),
            Negative_count=("sentiment_label", lambda x: (x == "Bearish").sum() + (x=="Somewhat-Bearish").sum()),
            Neutral_count=("sentiment_label", lambda x: (x=="Neutral").sum())).reset_index()
        news_df["Overall_confidence"] = news_df["Avg_positive_confidence"] + news_df["Avg_negative_confidence"]
        aggregated_news = news_df.set_index("bucket")
        return aggregated_news
      except Exception as e:
          print(f"Error: {e}")"""

"""def merge_data(price_df: pd.DataFrame, news_df: pd.DataFrame) -> pd.DataFrame:
    try:
        agg_news = aggregate_news(news_df)
        merged = pd.merge(price_df, agg_news, left_index = True, right_index = True, how="left")
        merged["Overall_confidence"] = merged["Overall_confidence"].fillna(0)
        merged["Headline_count"] = merged["Headline_count"].fillna(0)
        merged["Avg_positive_confidence"] = merged["Avg_positive_confidence"].fillna(0)
        merged["Avg_negative_confidence"] = merged["Avg_negative_confidence"].fillna(0)
        merged["Positive_count"] = merged["Positive_count"].fillna(0)
        merged["Negative_count"] = merged["Negative_count"].fillna(0)
        merged["Neutral_count"] = merged["Neutral_count"].fillna(0)
        return merged
    except Exception as e:
        print(f"Error: {e}")"""

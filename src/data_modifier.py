import pandas as pd



def clean_history(price_df: pd.DataFrame) -> pd.DataFrame:
    try:
        price_df = price_df.copy()
        price_df.dropna(subset=["Open", "Close", "High", "Low"], inplace=True)
        price_df["Volume"] = price_df["Volume"].fillna(0)
        price_df.sort_index(ascending = True, inplace=True)
        return price_df
    except Exception as e:
        print(f"Error cleaning stock price history: {e}")


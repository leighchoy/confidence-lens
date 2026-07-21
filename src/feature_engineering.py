from data_scraper import get_history
import pandas as pd
import ta

ticker = "NBIS"
interval = "1d"
start = "2026-01-01"
end = "2026-03-13"
#history = get_history(ticker, interval, start, end)

def tech_analysis(merged_df: pd.DataFrame) -> pd.DataFrame:
    merged_df = ta.add_all_ta_features(merged_df,open = "open",high= "High",low="Low",close="Close",volume="Volume",fillna=True)
    return merged_df


"""def feature_engineering(history):
    df = history.copy()

    df['return_5d'] = df['Close'].pct_change(5)
    df['return_10d'] = df['Close'].pct_change(10)
    df['return_20d'] = df['Close'].pct_change(20)

    df['volume_ratio'] = df['Volume'].div(df['Volume'].rolling(20).mean())
    df['sma_20'] = df['Close'].rolling(20).mean()
    df['dist_from_sma'] = (df['Close'] - df['sma_20']) / df['sma_20']

    #rsi
    delta = df['Close'].diff()
    gain = delta.clip(lower = 0).rolling(14).mean()
    loss = -delta.clip(upper = 0).rolling(14).mean()
    RS = gain/loss
    df['RSI'] = 100 - 100/(1+RS)
    df.dropna(inplace=True)

    return df


if history is not None and not history.empty:
    result = feature_engineering(history)
    print(result)
else:
    print("There is no history yet")
    """

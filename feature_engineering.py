from data_scraper import get_history

def feature_engineering(history):
    df = history.copy()

    df['return-5d'] = df['Close'].pct_change(5)
    df['return-10d'] = df['Close'].pct_change(10)
    df['return-20d'] = df['Close'].pct_change(20)

    df['volume_ratio'] = df['Volume'].div(df['Volume'].rolling(20).mean())
    df['sma_20d'] = df['Close'].rolling(20).mean()
    df['dis']
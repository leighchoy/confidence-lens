from config import processed_path, raw_path
import pandas as pd
import ta

from data_modifier import clean_history


def tech_analysis(merged_df: pd.DataFrame) -> pd.DataFrame:
    try:
        merged_df["ema_9"] = ta.trend.ema_indicator(merged_df["Close"],window = 9,fillna = True)
        merged_df["ema_26"] = ta.trend.ema_indicator(merged_df["Close"], window=26,fillna = True)


        #momentum TI's such as rsi and macd
        merged_df["rsi"] = ta.momentum.rsi(merged_df["Close"], window =14,fillna = True)
        merged_df["macd"] = ta.trend.macd_diff(merged_df["Close"],fillna = True)

        #volatility
        merged_df["atr"] = ta.volatility.average_true_range(merged_df["High"], merged_df["Low"], merged_df["Close"])
        merged_df["bollinger_high"] = ta.volatility.bollinger_hband(merged_df["Close"],fillna = True)
        merged_df["bollinger_low"] = ta.volatility.bollinger_lband(merged_df["Close"], fillna = True)

        #volume
        merged_df["obv"] = ta.volume.on_balance_volume(merged_df["Close"],merged_df["Volume"])

        merged_df["close_lag1"] = merged_df["Close"].shift(1)
        merged_df["close_lag2"] = merged_df["Close"].shift(2)
        merged_df["return_lag1"] = merged_df["Close"].pct_change(1)

        merged_df["target"] = (merged_df["Close"].shift(-10) > merged_df["Close"]).astype(int)

        merged_df = merged_df.dropna(subset =[ "close_lag1", "close_lag2", "return_lag1","target"])
        return merged_df
    except Exception as e:
        print(f"Error adding technical indicators: {e}")
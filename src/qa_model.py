import pandas as pd
from config import *

data_df = pd.DataFrame(
    pd.read_csv(processed_path("nbis_cash_flow.csv"))
)

def dcf(df:pd.DataFrame):
    forecast = df["free_cash_flow"]

    for i in range(1,df["fiscal_date"]):
        forecast.append(round(forecast[-1] + df))
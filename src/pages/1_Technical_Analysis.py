import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import *
import os

st.title("Technical Analysis")

fig = go.Figure()
ta_df = pd.DataFrame(pd.read_csv(processed_path("tech_analysis.csv")))
columns_to_drop = ["Volume", "target",
                   "return_lag1","close_lag1","close_lag2","obv",
                  "High","Low","Open","rsi","macd","atr"]
ta_df = ta_df.drop(columns = columns_to_drop)
ta_df.set_index("Date", inplace=True)

for i in ta_df.columns:
    ta_df[i] = pd.to_numeric(ta_df[i], errors="coerce")



choice = st.multiselect("Metrics", ta_df.columns.tolist())

for name in choice:

    if name in ta_df.columns:
        fig.add_trace(go.Scatter(x=ta_df.index, y=ta_df[name], name=name))

    else:
        st.warning(f"{name} not in data")

st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import processed_path
import os

from main import tech_analysis_df

st.title("Technical Analysis")

fig = go.Figure()
columns_to_drop = ["Volume", "target",
                   "return_lag1","close_lag1","close_lag2","obv",
                  "High","Low","Open","rsi","macd","atr"]
tech_analysis_df = st.session_state.tech_analysis_df
tech_analysis_df = tech_analysis_df.drop(columns = columns_to_drop)

for i in tech_analysis_df.columns:
    tech_analysis_df[i] = pd.to_numeric(tech_analysis_df[i], errors="coerce")



choice = st.multiselect("Metrics", tech_analysis_df.columns.tolist())

for name in choice:

    if name in tech_analysis_df.columns:
        fig.add_trace(go.Scatter(x=tech_analysis_df.index, y=tech_analysis_df[name], name=name))

    else:
        st.warning(f"{name} not in data")

st.plotly_chart(fig, use_container_width=True)

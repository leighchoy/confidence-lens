import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from charts import *
from config import *
import os
st.title("Technical Analysis")

def load_technical_metrics(pathname):
    df = pd.DataFrame(pd.read_csv(processed_path(pathname)))
    df.set_index('Date', inplace=True)
    for i in df.columns:
        df[i] = pd.to_numeric(df[i], errors='coerce')
    return df

fig = go.Figure()
df = load_technical_metrics("tech_analysis.csv")

choice = st.multiselect("Metrics", df.columns.tolist())

for name in choice:

    if name in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[name], name=name))

    else:
        st.warning(f"{name} not in data")

st.plotly_chart(fig, use_container_width=True)

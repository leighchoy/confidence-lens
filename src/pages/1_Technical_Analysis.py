import pandas as pd
import streamlit as st
from charts import *
import os
st.title("Technical Analysis")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "price_df.csv"))
fig = price_chart(df)
st.plotly_chart(fig, use_container_width=True)

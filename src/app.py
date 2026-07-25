import streamlit as st
from signal_model import *
import pandas as pd
from config import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed", "price_df.csv"),
                 index_col=0, parse_dates=True)

st.set_page_config(page_title="Confidence Scope", layout = "wide")

st.title("Confidence Scope")
st.subheader("Stock Rating Model")

with st.form("input_form"):
    col1,col2,col3 = st.columns(3)

    with col1:
        ticker= st.text_input("Enter ticker symbol", value =TICKER)

    with col2:
        start_date = st.date_input("Enter start date", value = START_DATE)
        end_date = st.date_input("Enter end date", value=END_DATE)

    with col3:
        timeframe = st.selectbox("Prediction Timeframe",
                                 ["10 Days", "20 days", "1 month", "3 months"])
        mode = st.radio("Signal Mode",
                        ["High Precision (fewer, more accurate signals)",
                         "High Recall (more signals, lower accuracy)"])

    submitted = st.form_submit_button("Analyse")
if submitted:
    st.divider()
    evaluate_model(df,"xgboost")

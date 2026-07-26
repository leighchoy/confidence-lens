import streamlit as st
from signal_model import *
import pandas as pd
from config import *

df = pd.DataFrame(pd.read_csv(processed_path("tech_analysis.csv")))

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
    prediction, probability = get_prediction(df)
    st.text("Model's Signal")
    if prediction == 1:
        st.success(f"Buy Signal - Model Confidence: {probability*100}%")
    else:
        st.warning(f"Hold/Sell Signal - Model's Probability of Positive Return in Timeframe: {probability*100}%")







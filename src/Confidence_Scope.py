import time
import traceback

import streamlit as st

from config import xgb_model, feature_cols, model_training_path
from feature_engineering import tech_analysis
from signal_model import get_prediction
import datetime
from language_model import get_lm_thesis
from fundamental_calculations import calculate_all
from data_scraper import *
from data_modifier import *



#@st.cache_data(ttl=3600)
def run_cs_model(ticker:str,start_date:str,end_date:str):
    price_df = get_history(ticker, start_date, end_date)
    price_df = clean_history(price_df)
    tech_analysis_df = tech_analysis(price_df)

    prediction, probability = get_prediction(xgb_model, feature_cols, tech_analysis_df)

    balance_df = get_balance_sheet(ticker)
    time.sleep(1.1)
    income_df = get_income_statement(ticker)
    time.sleep(1.1)
    cash_df = get_cash_flow(ticker)
    time.sleep(1.1)
    company_overview = get_company_overview(ticker)

    financials, dcf = calculate_all(balance_df, price_df, income_df, cash_df, company_overview)
    thesis = get_lm_thesis(ticker, financials, dcf, results_df, company_overview)

    return{
        "prediction":prediction,
        "probability":probability,
        "financials":financials,
        "thesis": thesis
    }

results_df = pd.DataFrame(pd.read_csv(model_training_path("trimmed_class_report_xgb.csv"),index_col = 0))
accuracy = results_df.loc["accuracy","precision"]
roc = results_df["ROC AUC"].iloc[0]

results_df = results_df.drop(index = "accuracy")
results_df = results_df.drop(columns = ["ROC AUC"])

st.set_page_config(page_title="Confidence Scope", layout = "wide")

st.title("Confidence Scope")
st.subheader("Stock Rating Model")
if "ticker" not in st.session_state:
    st.session_state.ticker = "NBIS"

if "start_date" not in st.session_state:
    st.session_state.start_date = datetime.date(2025, 12, 1)

if "end_date" not in st.session_state:
    st.session_state.end_date = datetime.date.today()

with st.form("input_form"):
    col1,col2 = st.columns(2)

    with col1:
        ticker= st.text_input("Enter ticker symbol", value =st.session_state.ticker)

    with col2:
        start_date = st.date_input("Enter start date", value = st.session_state.start_date)
        end_date = st.date_input("Enter end date", value=st.session_state.end_date)

    st.divider()
    if start_date >= end_date:
        st.error("Start date must be before end date")
        st.stop()
    if end_date <= start_date:
        st.error("End date must be before start date")
        st.stop()


    submitted = st.form_submit_button("Analyse")

if submitted:

    with st.spinner("Running analysis..."):
            #api callls
            try:
                results = run_cs_model(ticker,start_date,end_date)
            except Exception as e:
                st.error(f"Error: {e}")
                st.text(traceback.format_exc())
                st.stop()
            prediction = results["prediction"]
            probability = results["probability"]
            financials = results["financials"]
            thesis = results["thesis"]
            model_signal = {
                "Prediction":"Downward" if prediction < 0.5 else "Upward",
                "Probability of Upward Direction for 10-day Forecast":str(round(probability,5)),
                "ROC AUC":str(round(roc,4)),
                "Model Accuracy":str(round(accuracy,4))
            }

            st.session_state.ticker = ticker
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date

            st.session_state.results={
                "prediction": prediction,
                "probability": probability,
                "financials": financials,
                "thesis": thesis,
                "model_signal": model_signal
            }

    if "results" in st.session_state:
        results = st.session_state.results
        prediction = results["prediction"]
        probability = results["probability"]
        financials_display = results["financials"]
        thesis = results["thesis"]
        model_signal = results["model_signal"]

        fundamentals_display = pd.DataFrame([financials_display]).T
        fundamentals_display.columns = ["Value"]
        fundamentals_display["Value"] = fundamentals_display["Value"].astype(str)



        tab1,tab2,tab3= st.tabs(["Model's Investment Thesis","Fundamentals","Model Performance"])
        with tab1:
            st.markdown(thesis)
            st.divider()

        with tab2:
            st.dataframe(fundamentals_display,width="stretch")
        with tab3:
            st.dataframe(results_df)

            st.table(model_signal)

            st.divider()

            with st.expander("Class 0 and Class 1"):
                st.write("Class 0 represents downward price after forecast, Class 1 represents upward price after the forecast.")
            with st.expander("What does precision mean?"):
                st.write("How precise the model's prediction is."
                         "\ni.e. With a precision of .90, the model's prediction is correct 90% of the time.")
            with st.expander("What does recall mean?"):
                st.write("Out of all of the positive cases, how many did it predict correct?"
                         "\ni.e. With a recall of 0.75 for class 0, the model predicted 75% of all class 0's.")
            with st.expander("F1 Score"):
                st.write("How well does the model balance precision and recall?")
            with st.expander("Support"):
                st.write("The number of actual samples belonging to each class in the test set.")
            with st.expander("ROC AUC"):
                st.write("How well the model distinguishes between the two classes.\n"
                         "1.0 = perfect, 0.5 = random")
            with st.expander("Macro Average"):
                st.write("How the model performs across both classes on average.")
            with st.expander("Weighted Average"):
                st.write("How the model performs across both classes but weighted according to how many samples each class has.")
            st.divider()


st.page_link("pages/2_Model_Structure.py", label = "**Model Info**", icon ="ℹ️",icon_position = "right")




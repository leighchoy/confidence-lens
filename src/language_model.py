import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from config import *
from qa_model import calculate_all
from signal_model import get_prediction, xgb_model
import os
import traceback

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

results_df = pd.DataFrame(pd.read_csv(model_training_path("trimmed_class_report_xgb.csv")))
ta_df = pd.DataFrame(pd.read_csv(processed_path("tech_analysis.csv")))

#Senior Tech Equity Research Analyst
#classification_report = pd.DataFrame(pd.read_csv(processed_path(“classification_report”)))
def get_lm_thesis(ticker,financials,dcf,results_df,company_overview):
    try:

        prediction,probability = get_prediction(xgb_model,ta_df)
        ROC = results_df["ROC AUC"][1]
        precision  = results_df["precision"][1]
        recall  = results_df["recall"][1]
        macro_f1 = results_df["f1-score"][1]
        forecast = 10

        prompt = f"""You are a financial analyst assistant. 
        Based on the following data for {ticker}, provide a 
        clear investment interpretation for a retail investor. 
        
        A note: "Probability" reflects the model's certainty in its own classification, 
        not a literal probability of investment success. Phrase this 
        clearly for the reader.
        
        Company Name: {company_overview["Name"]}
        Description: {company_overview["Description"]}
        Sector: {company_overview["Sector"]}
        Industry: {company_overview["Industry"]}
        
        Forecast: {forecast}
        Prediction: {"BUY" if prediction == 1 else "DON'T BUY"}
        Probability of Buy (class 1): {probability:.1%}
    
        Model performance (historical reliability):
        ROC AUC: {ROC:.3f}
        Precision: {precision:.3f}
        Recall: {recall:.3f}
        Macro F1: {macro_f1:.3f}
        
              
        Fundamentals:
        Revenue CAGR: {financials["Revenue CAGR"]}
        Operating Margin: {financials["Operating Margin"]}
        Price/FCF: {financials["Price/Free Cash Flow"] if financials["Price/Free Cash Flow"] is float else f"Price/FCF not available: {financials["Price/Free Cash Flow"]}"}
        Price/OCF: {financials["Price/Operating Cash Flow"] if financials["Price/Operating Cash Flow"] is float else f"Price/OCF not available: {financials["Price/Operating Cash Flow"]}"}
        Debt/Equity: {financials["Debt/Equity"]}
        WACC: {financials['WACC']}
        FCF Growth: {financials["Free Cash Flow Growth"]}
        Prior FCF: {financials["Year Prior Free Cash Flow"]}
        FCF: {financials["Current Free Cash Flow"]}
        Market Cap: {financials["Market Cap"]}
        Beta: {financials["Beta"]}
        P/E: {financials["P/E"]}
        EPS: {financials["EPS"]}
        DCF VALUATION:
        {dcf["dcf_price_per_share"] if dcf.get('error') is None else f"DCF not available: {dcf['error']}"}
        
        Financial interpretation rules (STRICT):
        1.Debt leverage: If Debt/Equity is below 0.50, state that the company has low balance sheet debt. 
         never label Debt/Equity < 0.50 as "high debt" or "heavy debt burden". If cash flow is negative and no debt, label the risk 
        as "future equity dilution or capital-raise risk," not existing debt distress.
        
        2.Unprofitable valuation: If Operating Margin or EPS is negative, do NOT use P/E as a primary valuation indicator.
         Explain that the company is currently operating at a loss and focus on revenue growth vs cash burn rate.
         
        3.Model reliability: Explain ROC AUC as overall classification ability. Precision measures accuracy when 
         predicting buys (avoiding false alarms); Recall measures ability to catch all actual buy opportunities.
        
        Response instructions:
        Provide a clear 3-paragraph summary (approx. 6-8 sentences total) for a retail investor covering:
        1. Model Signal & Reliability: What the signal means and how reliable the model historically is.
        
        2. Fundamentals vs Signal: Whether high revenue growth aligns with or contradicts operational burn/margins and 
        provide context regarding the company and its industry.
        
        3. Key Risks & Horizons: Outline short-term volatility risks (Beta/CapEx) versus long-term execution/dilution risks. 
        Keep explanations simple without hallucinations.
        Number the topic explanations for readability."""

        completion = client.chat.completions.create(
            model = "openai/gpt-oss-20b",
            messages = [{"role": "user", "content": prompt}],
            temperature = 0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        traceback.print_exc()



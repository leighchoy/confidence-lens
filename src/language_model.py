import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from config import *
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

df = pd.DataFrame(pd.read_csv("../data/model_training/comparison_report.csv"))
results_df = pd.DataFrame(pd.read_csv("../data/model_training/trimmed_results_xgb.csv"))

completion = client.chat.completions.create(
    model = "llama-3.1-8b-instant",
    messages = [{"role": "user", "content": f"""You are a financial analyst assistant.
    Based on the following quantitative signals for {TICKER}, 
    Model prediction: {"BUY" if prediction == 1 else "SELL"}
    Confidence: {probability:.1%}
    provide a brief investment interpretatio.Provide a 3-4 sentence interpretation suitable 
    for a retail investor."""
                 }],
    temperature = 0.75
)
print(completion.choices[0].message.content)




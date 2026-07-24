from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, \
    roc_auc_score, mean_squared_error
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from config import *

import xgboost as xgb
import seaborn as sns

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from news_scraper import model

df = pd.read_csv("../data/processed/tech_analysis.csv", index_col=0, parse_dates=True)

"""
Helper function to drop features and split data in 80/20 split.
Not using randomised split as future data would help the model predict in a more biased manner.
"""

def create_dummy(X_train,X_test, y_train, y_test):
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_train, y_train)
    dummy_pred = dummy.predict(X_test)


    dummy = pd.DataFrame(classification_report(y_test,dummy_pred,output_dict = True)).T
    dummy.to_csv("../data/model_training/dummy.csv")

def prepare_data(df : pd.DataFrame):
    split = int(len(df) * 0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]
    """
    Least important features for logisitic regression:
    "ema_26","Neutral_count","ema_9","Avg_positive_confidence", "return_lag1", "Negative_count"
    ,"Headline_count", "close_lag2", "close_lag1", "obv", "bollinger_low"
    , "bollinger_high", "Overall_confidence", "Avg_negative_confidence"
    , "Avg_negative_confidence","Positive_count" ,"sentiment_lag1"
    
    Least important for rf
    "target", "Close", "High", "Low", "Open",
    "Volume","Neutral_count","Avg_positive_confidence", "return_lag1", "Negative_count"
    ,"Headline_count", "close_lag2", "close_lag1", "obv"
    , "bollinger_high", "Overall_confidence", "Avg_negative_confidence"
    , "Avg_negative_confidence","Positive_count" ,"sentiment_lag1"
     
    Sentiment features:
    "Avg_positive_confidence", "Avg_negative_confidence",
    "Headline_count", "Positive_count", "Negative_count",
    "Neutral_count", "Overall_confidence", "sentiment_lag1"
    
    Price features:
    "macd","ema_9","ema_26","rsi","bollinger_high","bollinger_low",
    "close_lag2","close_lag1","return_lag1","obv","atr",
    
    """
    drop_cols = [
    "target", "Close", "High", "Low", "Open",
    "Volume","Neutral_count","Avg_positive_confidence", "return_lag1", "Negative_count"
    ,"Headline_count", "close_lag2", "close_lag1", "obv"
    , "bollinger_high", "Overall_confidence", "Avg_negative_confidence"
    , "Avg_negative_confidence","Positive_count" ,"sentiment_lag1"
    ]

    X_train = train.drop(columns=drop_cols)
    X_test = test.drop(columns=drop_cols)
    y_train = train["target"]
    y_test = test["target"]

    return X_train, X_test, test, train, y_train, y_test

"""
Using logistic regression as baseline.
"""
def train_model_lr(df: pd.DataFrame):
    X_train, X_test, test, train, y_train, y_test = prepare_data(df)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    """
    C value of 0.01 makes the model predict class 1 for each test.
    C value of 1.0 in comparison to 0.1 is overall weaker with
    obvious disadvantages being lower recall and lower precision
    """
    model = LogisticRegression(
        C=c,
        penalty= "l1" or "l2",
        solver= "liblinear" or "saga",
        class_weight= None or "balanced",
        max_iter= 1000

    )
    """
    Having class_weight set to just balanced creates better class 
    1 recall but hurts macro f1, ROC and precision values.
    
    Tested alternative thresholds to improve recall values with 
    class_weight set to None or "balanced".
    """
    model.fit(X_train_scaled, y_train)


    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    """
    Threshold of 0.5 produces a precision of 1.0 whilst generating buy signals for 
    10/41 of actual class 1's.
    This results in losing around 75% of buying opportunities.
    
    A threshold of 0.4 captures 87.8% of actual class 1's retaining a
    precision score of 0.722.
    
    Can have both as an option of a high-confidence signal (0.5)
    or a boosted recall signal (0.4).
    """
    y_pred = (y_prob >= THRESHOLD).astype(int)
    total_days = y_test.sum()

    """print("Threshold\tROC\tF1\tRecall\tPrecision")
    for threshold in (0.3, 0.35, 0.4, 0.45,0.49, 0.5):
        y_pred = (y_prob >= threshold).astype(int)
        buy_signals = y_pred.sum()
        print(threshold,"\t",
        round(roc_auc_score(y_test, y_prob),3),"\t",
        round((f1_score(y_test,y_pred)),3),"\t",
        round((recall_score(y_test,y_pred)),3),"\t",
        round((precision_score(y_test,y_pred)),3),"\t",
        buy_signals,"\t",total_days)
    print(y_test.value_counts())"""

    create_dummy(X_train, X_test, y_train, y_test)

    return model, y_pred, y_prob

def train_model_rf(df : pd.DataFrame):
    X_train, X_test, test, train, y_train, y_test = prepare_data(df)

    total_days = y_test.sum()
    print("Threshold ROC\tF1\tRecall\tPrecision")

    model = RandomForestClassifier(
    n_estimators=100,
    max_depth=3,
    min_samples_split=5,
    min_samples_leaf=4,
    random_state=42
    )

    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    threshold = 0.4
    #for threshold in[0.3,0.35,0.4,0.45,0.5,0.55]:
    y_pred = (y_prob >= threshold).astype(int)

    buy_signals = y_pred.sum()


    return model, y_pred, y_prob

def train_model_xgb(df: pd.DataFrame):
    X_train,X_test,test, train,y_train,y_test = prepare_data(df)
    total_days = y_test.sum()
    print("Threshold ROC\tF1\tRecall\tPrecision")
    #for n in[0.01,0.1,0.2,0.3,0.5]:
    model = XGBClassifier(

                    max_depth=3,
                n_estimators=100,
                    min_child_weight = 1,
                    gamma = 0.01,
                learning_rate=0.3,
                random_state=42


    )
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    threshold = 0.25
        #for threshold in[0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55]:
    y_pred = (y_prob >= threshold).astype(int)

    buy_signals = y_pred.sum()

    return model, y_pred, y_prob

def append_summary_row (results, model_name, config_name, y_test, y_pred, y_prob):
    buy_signals = y_pred.sum()
    total_days = len(y_pred)
    signal_ratio = buy_signals / total_days
    results.append({
        "Model": model_name,
        "Config": config_name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Macro F1": f1_score(y_test, y_pred, average="macro"),
        "Class 1 Precision": precision_score(y_test, y_pred, pos_label=1),
        "Class 1 Recall": recall_score(y_test, y_pred, pos_label=1),
        "Class 1 F1": f1_score(y_test, y_pred, pos_label=1),
        "ROC AUC": roc_auc_score(y_test, y_prob),
        "Signal Ratio": signal_ratio,
        "Total Days": total_days,
        "Buy Signals": buy_signals
    })


def evaluate_model(df : pd.DataFrame):
    X_train, X_test, test, train, y_train, y_test = prepare_data(df)

    model, y_pred , y_prob= train_model_xgb(df)
    class_report = pd.DataFrame(classification_report(y_test, y_pred,output_dict=True)).T
    class_report["ROC AUC"] = roc_auc_score(y_test, y_prob)
    class_report["Model"] = model.__class__.__name__

    print("Accuracy Test\n", accuracy_score(y_test, y_pred))

    class_report.to_csv("../data/model_training/trimmed_class_report_xgb.csv", index=True)

    buy_signals = y_pred.sum()
    total_days = len(y_pred)
    signal_ratio = buy_signals / total_days


    results = pd.DataFrame({
        "Prediction" : y_pred,
        "Probability" : y_prob,
        "Actual" : y_test
    })
    results.to_csv("../data/model_training/trimmed_results_xgb.csv", index=False)
    importance = pd.DataFrame({
        "feature": X_train.columns,
        "importance": model.feature_importances_  # abs value since negative = predicts down
    }).sort_values("importance", ascending=False)

    plt.figure(figsize=(10, 10))
    plt.title('Feature Importance)')
    plt.barh(importance["feature"], importance["importance"])
    plt.xlabel('Coefficient magnitude')
    plt.tight_layout()

    plt.savefig('../data/pngs/trimmed_feature_importance_rxgb.png')

    """coef = pd.DataFrame({
        "feature": X_train.columns,
        "magnitude": abs(model.coef_[0]) ,
        "coefficient": (model.coef_[0]),
    }).sort_values("magnitude", ascending=False)"""

    #plt.savefig('../data/pngs/coef.png')


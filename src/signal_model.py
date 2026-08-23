import traceback

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, \
    roc_auc_score
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import xgboost
from config import xgb_model, c, THRESHOLD, feature_cols, processed_path

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt



ta_df = pd.DataFrame(pd.read_csv(processed_path("tech_analysis.csv")))
"""
Helper function to drop features and split data in 80/20 split.
Not using randomised split as future data would help the model predict in a more biased manner.
"""

def create_dummy(X_train,X_test, y_train, y_test) -> None:
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_train, y_train)
    dummy_pred = dummy.predict(X_test)


    dummy = pd.DataFrame(classification_report(y_test,dummy_pred,output_dict = True)).T
    dummy.to_csv("../data/model_training/dummy.csv")

def prepare_data(df : pd.DataFrame)->tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

    split = int(len(df) * 0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]

    drop_cols = ["Date",
    "target", "Close", "High", "Low", "Open",
    "Volume", "return_lag1",  "close_lag2", "close_lag1", "obv"
    , "bollinger_high"
    ]

    X_train = train.drop(columns=drop_cols).reset_index(drop=True)
    X_test = test.drop(columns=drop_cols).reset_index(drop=True)

    y_train = train["target"]
    y_test = test["target"]

    return X_train, X_test, test, train, y_train, y_test

"""
Using logistic regression as baseline.
"""
def train_model_lr(df:pd.DataFrame):

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
        penalty= "l1",
        solver= "liblinear",
        class_weight= None,
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

    create_dummy(X_train, X_test, y_train, y_test)

    return model, y_pred, y_prob

def train_model_rf(df:pd.DataFrame):

    X_train, X_test, test, train, y_train, y_test = prepare_data(df)

    total_days = y_test.sum()
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
    y_pred = (y_prob >= threshold).astype(int)

    buy_signals = y_pred.sum()


    return model, y_pred, y_prob

def train_model_xgb(df:pd.DataFrame) -> tuple[XGBClassifier,int,float,pd.DataFrame,pd.DataFrame]:

    X_train,X_test,test, train,y_train,y_test = prepare_data(df)
    total_days = y_test.sum()
    model = XGBClassifier(

                    max_depth=3,
                n_estimators=100,
                    min_child_weight = 1,
                    gamma = 0.01,
                learning_rate=0.3,
                random_state=42


    )
    model.fit(X_train, y_train)
    model.save_model("../src/models/xgb_model.json")

    y_prob = model.predict_proba(X_test)[:, 1]
    threshold = 0.25
    y_pred = (y_prob >= threshold).astype(int)

    buy_signals = y_pred.sum()

    return model, y_pred, y_prob, X_test, X_train


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


def evaluate_model(df : pd.DataFrame) -> pd.DataFrame:
    X_train, X_test, test, train, y_train, y_test = prepare_data(df)

    model, y_pred , y_prob,_,_= train_model_xgb(df)


    class_report = pd.DataFrame(classification_report(y_test, y_pred,output_dict=True)).T
    class_report["ROC AUC"] = roc_auc_score(y_test, y_prob)
    class_report["Model"] = model.__class__.__name__


    return class_report

def get_prediction(model,feature_cols,X : pd.DataFrame,threshold : float = 0.4)-> tuple[int,float]:
    try:
        X = X[feature_cols]
        latest = X.iloc[[-1]]
        probability = model.predict_proba(latest)[0][1]
        prediction = 1 if probability >= threshold else 0
        return prediction, probability
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())


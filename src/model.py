from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, \
    roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor as rf
import xgboost as xgb
import seaborn as sns

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



df = pd.read_csv("../data/processed/tech_analysis.csv", index_col=0, parse_dates=True)

"""
Helper function to drop features and split data in 80/20 split.
Not using randomised split as future data would help the model predict in a more biased manner.
"""
def prepare_data(df : pd.DataFrame):
    split = int(len(df) * 0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]

    drop_cols = ["target", "Close", "High", "Low", "Open", "Volume"]
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
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    return model, y_pred, y_prob

def train_model_xgb(df : pd.DataFrame):
    X_train, X_test, test, train, y_train, y_test = prepare_data(df)




def evaluate_model(df : pd.DataFrame):
    X_train, X_test, test, train, y_train, y_test = prepare_data(df)

    model, y_pred , y_prob= train_model_lr(df)
    class_report = pd.DataFrame(classification_report(y_test, y_pred,output_dict=True)).T
    class_report["ROC AUC"] = roc_auc_score(y_test, y_prob)
    class_report["Model"] = model.__class__.__name__

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    class_report.to_csv("../data/processed/class_report.csv", index=True)

    summary_report = pd.DataFrame({
        "Model" : [model.__class__.__name__],
        "Recall" : [recall_score(y_test, y_pred)],
        "Accuracy" : [accuracy_score(y_test, y_pred)],
        "Precision": [precision_score(y_test, y_pred)],
        "F1" : [f1_score(y_test, y_pred)],
        "ROC AUC" : [roc_auc_score(y_test, y_prob)]

    })
    summary_report.to_csv("../data/processed/summary_report.csv", index=False)

    importance = pd.DataFrame({
        "feature": X_train.columns,
        "importance": abs(model.coef_[0])  # abs value since negative = predicts down
    })
    importance = importance.sort_values("importance", ascending=False)

    plt.figure(figsize=(10, 10))
    plt.title('Feature Importance)')
    plt.barh(importance["feature"], importance["importance"])
    plt.xlabel('Coefficient magnitude')
    plt.tight_layout()

    plt.savefig('../data/processed/feature_importance.png')

def compare_models(df : pd.DataFrame):
    X_train, X_test, test, train, y_train, y_test = prepare_data(df)
    lr_model, y_pred_lr, y_prob_lr = train_model_xgb(df)

evaluate_model(df)

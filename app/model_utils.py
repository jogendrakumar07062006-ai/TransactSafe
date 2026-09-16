# app/model_utils.py

import os
import joblib
import pandas as pd
from app.config import MODEL_PATH

_MODEL_FULL_PATH = os.path.join(os.path.dirname(__file__), "..", MODEL_PATH)
_pipeline = None

def load_model():
    global _pipeline
    if _pipeline is None:
        _pipeline = joblib.load(_MODEL_FULL_PATH)
    return _pipeline

def predict_fraud_probability(transaction_dict: dict) -> float:
    pipeline = load_model()

    tx = dict(transaction_dict)
    tx["Hour"] = (tx["Time"] % 86400) // 3600
    tx["IsNight"] = 1 <= tx["Hour"] <= 5

    X = pd.DataFrame([tx])
    X = X.drop(columns=["Time"], errors="ignore")

    return float(pipeline.predict_proba(X)[:, 1][0])

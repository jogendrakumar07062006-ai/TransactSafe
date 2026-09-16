# utils.py

import os
import joblib
import pandas as pd
import numpy as np
import time
from groq import Groq
from app.config import (
    MODEL_PATH, 
    GROQ_MODEL_HIGH, 
    GROQ_MODEL_MEDIUM,
    RULE_LOW_AMOUNT_THRESHOLD,
    RULE_NIGHT_HOUR_START,
    RULE_NIGHT_HOUR_END,
    TIER_HIGH_THRESHOLD,
    TIER_MEDIUM_THRESHOLD
)

_MODEL_FULL_PATH = os.path.join(os.path.dirname(__file__), MODEL_PATH)
_pipeline = None

# ----------------- ML INFERENCE -----------------
def load_model():
    global _pipeline
    if _pipeline is None:
        _pipeline = joblib.load(_MODEL_FULL_PATH)
    return _pipeline

# Expected feature order by the trained model
EXPECTED_FEATURES = [f"V{i}" for i in range(1, 29)] + ["Amount", "Hour", "IsNight"]

def predict_fraud_probability(tx_dict: dict) -> float:
    pipeline = load_model()
    # Deriving needed features
    tx = dict(tx_dict)
    if "Hour" not in tx and "Time" in tx:
        tx["Hour"] = (tx["Time"] % 86400) // 3600
    if "IsNight" not in tx and "Hour" in tx:
        tx["IsNight"] = int(1 <= tx["Hour"] <= 5)
        
    # Ensure expected order for pipeline if needed
    X = pd.DataFrame([tx])
    
    # Reorder to match model expectations exactly
    for col in EXPECTED_FEATURES:
        if col not in X.columns:
            X[col] = 0.0 # Safety fallback
    X = X[EXPECTED_FEATURES]
    
    return float(pipeline.predict_proba(X)[:, 1][0])

def predict_batch(df: pd.DataFrame) -> np.ndarray:
    pipeline = load_model()
    # Process dataframe
    df_proc = df.copy()
    if "Hour" not in df_proc.columns and "Time" in df_proc.columns:
        df_proc["Hour"] = (df_proc["Time"] % 86400) // 3600
    if "IsNight" not in df_proc.columns and "Hour" in df_proc.columns:
        df_proc["IsNight"] = df_proc["Hour"].between(1, 5).astype(int)
    
    # Reorder to match model expectations exactly
    for col in EXPECTED_FEATURES:
        if col not in df_proc.columns:
            df_proc[col] = 0.0 # Safety fallback
    df_proc = df_proc[EXPECTED_FEATURES]
        
    return pipeline.predict_proba(df_proc)[:, 1]

# ----------------- RULE ENGINE -----------------
def rule_low_amount(amount: float) -> bool:
    return amount < RULE_LOW_AMOUNT_THRESHOLD

def rule_night_hour(hour: int) -> bool:
    return RULE_NIGHT_HOUR_START <= hour <= RULE_NIGHT_HOUR_END

def evaluate_rules(tx_dict: dict):
    amount = tx_dict.get("Amount", 0)
    hour = tx_dict.get("Hour", 0)
    if "Hour" not in tx_dict and "Time" in tx_dict:
        hour = (tx_dict["Time"] % 86400) // 3600
    
    return {
        "low_amount": rule_low_amount(amount),
        "night_hour": rule_night_hour(hour)
    }

def assign_tier(ml_prob: float, flags: dict) -> str:
    if ml_prob >= TIER_HIGH_THRESHOLD:
        tier = "high"
    elif ml_prob >= TIER_MEDIUM_THRESHOLD:
        tier = "medium"
    else:
        tier = "low"

    # Rule Escalation
    if tier == "low" and flags.get("low_amount") and flags.get("night_hour"):
        tier = "medium"
    return tier

# ----------------- LLM INTEGRATION -----------------
def get_explanation(tier: str, amount: float, hour: int, ml_prob: float, flags: dict):
    if tier == "low":
        return {"text": None, "provider": None, "latency": 0.0}
        
    prompt = (
        f"A transaction was flagged as risk (model score: {ml_prob:.2f}). "
        f"Amount: ${amount:.2f}, Hour: {int(hour)}:00. "
        f"Low-amount flag: {flags.get('low_amount')}. Night-hour flag: {flags.get('night_hour')}. "
        "In 2-3 plain-English sentences, explain the risk factors a fraud analyst should know, "
        "without claiming to know the model's internal reasoning."
    )
    
    model = GROQ_MODEL_HIGH if tier == "high" else GROQ_MODEL_MEDIUM
    
    try:
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        start_time = time.time()
        response = groq_client.chat.completions.create(
            model=model,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
        latency = round((time.time() - start_time) * 1000, 1)
        provider = f"groq/{model}"
    except Exception as e:
        # Deterministic fallback if API fails/missing
        start_time = time.time()
        time.sleep(0.1) # Simulate logic latency
        text = f"Automated Heuristic: High predicted probability ({ml_prob:.2f}). "
        if flags.get('night_hour'):
            text += "Transaction occurred during suspicious late-night hours. "
        if flags.get('low_amount'):
            text += "Transaction amount is unusually low, often indicating card testing. "
        text += "Further review recommended."
        latency = round((time.time() - start_time) * 1000, 1)
        provider = "local/heuristic"

    return {"text": text, "provider": provider, "latency": latency}

# ----------------- GENERATORS -----------------
def get_preset_transaction(preset_type: str) -> dict:
    # Base legitimate template
    tx = {f"V{i}": 0.0 for i in range(1, 29)}
    tx["Time"] = 45000.0
    tx["Amount"] = 150.0
    
    if preset_type == "Legitimate":
        tx["V1"], tx["V2"] = 1.2, -0.5
        tx["Hour"] = 14
        tx["Amount"] = 45.50
    elif preset_type == "Night Micro-transaction":
        tx["Hour"] = 3
        tx["Amount"] = 1.50
        tx["V1"], tx["V2"], tx["V3"] = -1.5, 2.5, -1.0
    elif preset_type == "High-Value Fraud":
        # Simulate extreme PCA deviations
        for i in range(1, 10):
            tx[f"V{i}"] = -10.0 + (i * 1.5)
        tx["Hour"] = 2
        tx["Amount"] = 9500.00
        
    return tx

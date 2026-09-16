# app/main.py

from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.schemas import TransactionRequest, ScoreResponse, RuleFlags
from app.model_utils import predict_fraud_probability
from app.rules import rule_low_amount, rule_night_hour, assign_tier
from app.llm_explain import get_explanation
from app.storage import save_transaction, get_all_transactions

app = FastAPI(title="TransactSafe")

@app.post("/score-transaction", response_model=ScoreResponse)
def score_transaction(transaction: TransactionRequest):
    tx = transaction.model_dump()
    hour = (tx["Time"] % 86400) // 3600

    ml_probability = predict_fraud_probability(tx)
    low_amount = rule_low_amount(tx["Amount"])
    night_hour = rule_night_hour(hour)
    tier = assign_tier(ml_probability, low_amount, night_hour)

    explanation = get_explanation(tier, tx["Amount"], hour, ml_probability, low_amount, night_hour)

    result = {
        "ml_probability": round(ml_probability, 4),
        "tier": tier,
        "rule_flags": RuleFlags(low_amount=low_amount, night_hour=night_hour),
        "explanation": explanation["text"],
        "latency_ms": explanation["latency_ms"],
        "cost_usd": explanation["cost_usd"],
        "provider": explanation["provider"],
    }
    save_transaction({**tx, **result})
    return result


@app.get("/transactions")
def list_transactions():
    return get_all_transactions()

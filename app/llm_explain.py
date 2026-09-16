import os
import time
from groq import Groq
from app.config import GROQ_MODEL_HIGH, GROQ_MODEL_MEDIUM

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(amount, hour, ml_probability, low_amount, night_hour):
    return (
        f"A transaction was flagged as risk (model score: {ml_probability:.2f}). "
        f"Amount: ${amount:.2f}, Hour: {int(hour)}:00. "
        f"Low-amount flag: {low_amount}. Night-hour flag: {night_hour}. "
        "In 2-3 plain-English sentences, explain the risk factors a fraud analyst should know, "
        "without claiming to know the model's internal reasoning."
    )


def _call_groq(prompt, model, tier):
    start = time.time()
    response = groq_client.chat.completions.create(
        model=model, max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content or "Explanation unavailable (token budget exceeded)."
    return {
        "text": text,
        "latency_ms": round((time.time() - start) * 1000, 1),
        "cost_usd": 0.0,
        "provider": f"groq/{model}",
        "tier": tier
    }


def get_explanation(tier, amount, hour, ml_probability, low_amount, night_hour):
    prompt = build_prompt(amount, hour, ml_probability, low_amount, night_hour)
    if tier == "high":
        return _call_groq(prompt, GROQ_MODEL_HIGH, "high")
    elif tier == "medium":
        return _call_groq(prompt, GROQ_MODEL_MEDIUM, "medium")
    return {"text": None, "latency_ms": 0.0, "cost_usd": 0.0, "provider": None, "tier": "low"}

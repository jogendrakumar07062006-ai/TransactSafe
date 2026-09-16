# app/rules.py

from app.config import RULE_LOW_AMOUNT_THRESHOLD, RULE_NIGHT_HOUR_START, RULE_NIGHT_HOUR_END

def rule_low_amount(amount: float) -> bool:
    return amount < RULE_LOW_AMOUNT_THRESHOLD

def rule_night_hour(hour: int) -> bool:
    return RULE_NIGHT_HOUR_START <= hour <= RULE_NIGHT_HOUR_END

def assign_tier(ml_probability: float, low_amount: bool, night_hour: bool) -> str:
    from app.config import TIER_HIGH_THRESHOLD, TIER_MEDIUM_THRESHOLD

    if ml_probability >= TIER_HIGH_THRESHOLD:
        tier = "high"
    elif ml_probability >= TIER_MEDIUM_THRESHOLD:
        tier = "medium"
    else:
        tier = "low"

    if tier == "low" and low_amount and night_hour:
        tier = "medium"

    return tier

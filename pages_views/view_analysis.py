# pages_views/view_analysis.py

import streamlit as st
import json
from utils import get_preset_transaction, predict_fraud_probability, evaluate_rules, assign_tier, get_explanation
from styles import risk_badge_html, ai_card_html
from charts import create_risk_gauge
from app.storage import save_transaction

def render():
    st.title("🔍 Single Transaction Analysis")
    st.markdown("Score a transaction in real-time. Enter details manually or load a synthetic preset.")
    
    # Preset Selector
    preset = st.radio(
        "Load Preset Profile:",
        ["Legitimate", "Night Micro-transaction", "High-Value Fraud", "Manual"],
        horizontal=True
    )
    
    if preset != "Manual":
        st.session_state["tx_form"] = get_preset_transaction(preset)
    elif "tx_form" not in st.session_state:
        st.session_state["tx_form"] = get_preset_transaction("Legitimate")
        
    tx_data = st.session_state["tx_form"]
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount ($)", value=float(tx_data.get("Amount", 0.0)), step=1.0)
            hour = st.number_input("Hour of Day (0-23)", value=int(tx_data.get("Hour", 12)), min_value=0, max_value=23)
        with col2:
            v1 = st.number_input("PCA V1", value=float(tx_data.get("V1", 0.0)))
            v2 = st.number_input("PCA V2", value=float(tx_data.get("V2", 0.0)))
            
        with st.expander("Advanced PCA Features (V3 - V28)"):
            c1, c2, c3, c4 = st.columns(4)
            v_dict = {}
            for i in range(3, 29):
                # Distribute inputs across columns
                col = [c1, c2, c3, c4][(i-3) % 4]
                with col:
                    v_dict[f"V{i}"] = st.number_input(f"V{i}", value=float(tx_data.get(f"V{i}", 0.0)), step=0.1)
                    
        submit = st.form_submit_button("Analyze Transaction", use_container_width=True)
        
    if submit:
        # Build payload
        payload = {"Amount": amount, "Hour": hour, "V1": v1, "V2": v2}
        payload.update(v_dict)
        
        with st.spinner("Running ML Inference & Rules..."):
            ml_prob = predict_fraud_probability(payload)
            rule_flags = evaluate_rules(payload)
            tier = assign_tier(ml_prob, rule_flags)
            
        with st.spinner("Requesting AI Analyst Explanation..."):
            explanation = get_explanation(tier, amount, hour, ml_prob, rule_flags)
            
        # Save record
        record = {
            **payload,
            "ml_probability": ml_prob,
            "tier": tier,
            "rule_flags": rule_flags,
            "explanation": explanation["text"],
            "latency_ms": explanation["latency"],
            "provider": explanation["provider"]
        }
        save_transaction(record)
        
        # Display Results
        st.markdown("---")
        st.subheader("Analysis Results")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.plotly_chart(create_risk_gauge(ml_prob), use_container_width=True)
            st.markdown(risk_badge_html(tier), unsafe_allow_html=True)
            
        with c2:
            st.markdown("#### Triggered Rules")
            if rule_flags["low_amount"]:
                st.markdown("✅ **Low Amount Flag** (< $5.00)")
            if rule_flags["night_hour"]:
                st.markdown("✅ **Night Hour Flag** (01:00 - 05:00)")
            if not rule_flags["low_amount"] and not rule_flags["night_hour"]:
                st.markdown("No basic heuristic rules triggered.")
                
            if explanation["text"]:
                st.markdown(ai_card_html(explanation["text"], explanation["provider"], explanation["latency"]), unsafe_allow_html=True)

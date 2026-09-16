# pages_views/view_dashboard.py

import streamlit as st
import pandas as pd
from app.storage import get_all_transactions
from charts import create_fraud_donut_chart, create_hourly_fraud_chart, create_risk_histogram
from styles import risk_badge_html

def render():
    st.title("📊 Global SOC Dashboard")
    st.markdown("Real-time overview of transaction processing, ML inferences, and fraud metrics.")
    
    transactions = get_all_transactions()
    if not transactions:
        st.info("No transactions processed yet. Visit **Transaction Analysis** or **Batch Analysis** to score data.")
        return
        
    df = pd.DataFrame(transactions)
    
    # KPI Metrics Calculation
    total_tx = len(df)
    fraud_count = len(df[df["tier"] == "high"])
    fraud_rate = (fraud_count / total_tx) * 100 if total_tx > 0 else 0
    avg_risk = df["ml_probability"].mean()
    avg_latency = df["latency_ms"].mean() if "latency_ms" in df.columns else 0
    
    # Render KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", f"{total_tx:,}")
    col2.metric("Fraudulent (High Risk)", f"{fraud_count:,}", delta=f"{fraud_rate:.1f}%", delta_color="inverse")
    col3.metric("Avg Risk Score", f"{avg_risk:.3f}")
    col4.metric("Avg LLM Latency", f"{avg_latency:.0f} ms" if avg_latency else "N/A")
    
    st.markdown("---")
    
    # Charts Grid
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_fraud_donut_chart(df), use_container_width=True)
        if "Hour" in df.columns:
            st.plotly_chart(create_hourly_fraud_chart(df), use_container_width=True)
    with c2:
        st.plotly_chart(create_risk_histogram(df), use_container_width=True)
    
    st.markdown("### Recent Transactions Feed")
    
    # Display recent transactions in table
    display_df = df.copy().tail(20).iloc[::-1] # Last 20, newest first
    display_df["Risk Tier"] = display_df["tier"].apply(lambda t: t.upper())
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"${x:.2f}")
    display_df["Score"] = display_df["ml_probability"].apply(lambda x: f"{x:.4f}")
    
    # Rules formatting
    if "rule_flags" in display_df.columns:
        display_df["Rules"] = display_df["rule_flags"].apply(
            lambda f: ", ".join([k for k, v in f.items() if v]) if isinstance(f, dict) else "None"
        )
    else:
        display_df["Rules"] = "None"
        
    cols_to_show = ["Risk Tier", "Score", "Amount", "Hour", "Rules", "provider"]
    available_cols = [c for c in cols_to_show if c in display_df.columns]
    
    st.dataframe(display_df[available_cols], use_container_width=True)

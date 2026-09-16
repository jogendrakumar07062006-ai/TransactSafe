# pages_views/view_batch.py

import streamlit as st
import pandas as pd
import time
from utils import predict_batch, evaluate_rules, assign_tier
from app.storage import save_transaction

def render():
    st.title("📁 Batch Analysis")
    st.markdown("Upload a CSV file containing transaction data for high-throughput batch scoring.")
    if "demo_loaded" not in st.session_state:
        st.session_state.demo_loaded = False
        
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file is not None:
            st.session_state.demo_loaded = False
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Load Demo Dataset", use_container_width=True):
            st.session_state.demo_loaded = True
            
    # Determine the file to process
    file_to_process = uploaded_file
    if st.session_state.demo_loaded:
        file_to_process = "data/sample_transactions.csv"
            
    if file_to_process:
        try:
            df = pd.read_csv(file_to_process)
            st.success(f"Loaded {len(df)} transactions.")
            
            if st.button("Start Batch Analysis", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Predict all probabilities at once (vectorized)
                status_text.text("Running ML Inference...")
                probs = predict_batch(df)
                df["ml_probability"] = probs
                
                # Rule Engine evaluation (iterative or vectorized, keeping it simple iteratively for rules)
                status_text.text("Evaluating Heuristic Rules & Assigning Tiers...")
                tiers = []
                rule_flags_list = []
                
                for i in range(len(df)):
                    row = df.iloc[i].to_dict()
                    rules = evaluate_rules(row)
                    tier = assign_tier(row["ml_probability"], rules)
                    
                    tiers.append(tier)
                    rule_flags_list.append(rules)
                    
                    # Update progress UI every 10% to avoid freezing
                    if i % max(1, len(df)//10) == 0:
                        progress_bar.progress(int((i/len(df))*100))
                
                df["tier"] = tiers
                df["rule_flags"] = rule_flags_list
                progress_bar.progress(100)
                status_text.text("Batch Analysis Complete!")
                
                # Save to global storage
                for i in range(len(df)):
                    record = df.iloc[i].to_dict()
                    save_transaction(record)
                    
                # Results Overview
                fraud_count = len(df[df['tier'] == 'high'])
                med_count = len(df[df['tier'] == 'medium'])
                
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                c1.metric("Scored Transactions", len(df))
                c2.metric("High Fraud Risk", fraud_count, delta_color="inverse")
                c3.metric("Medium Risk", med_count, delta_color="inverse")
                
                # Highlight rows
                def color_rows(row):
                    if row['tier'] == 'high':
                        return ['background-color: rgba(239, 68, 68, 0.2)'] * len(row)
                    elif row['tier'] == 'medium':
                        return ['background-color: rgba(245, 158, 11, 0.2)'] * len(row)
                    return [''] * len(row)
                
                display_cols = ["Amount", "ml_probability", "tier"] + [c for c in df.columns if c.startswith("V")][:5]
                styled_df = df[display_cols].style.apply(color_rows, axis=1)
                
                st.dataframe(styled_df, use_container_width=True)
                
                # Export
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Analyzed Results",
                    csv,
                    "batch_results.csv",
                    "text/csv",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"Error processing batch: {e}")

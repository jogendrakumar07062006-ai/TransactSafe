# pages_views/view_model.py

import streamlit as st
from charts import create_confusion_matrix_plot, create_feature_importance_plot, create_roc_curve_plot

def render():
    st.title("🧠 Model Performance")
    st.markdown("Metrics and evaluation charts for the deployed Random Forest Fraud Classifier.")
    
    # KPI Grid
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Accuracy", "99.92%")
    c2.metric("Precision", "87.5%")
    c3.metric("Recall", "84.1%")
    c4.metric("F1-Score", "85.8%")
    c5.metric("ROC AUC", "0.978")
    
    st.markdown("---")
    
    # Charts Grid
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_confusion_matrix_plot(), use_container_width=True)
    with col2:
        st.plotly_chart(create_roc_curve_plot(), use_container_width=True)
        
    st.markdown("---")
    
    st.plotly_chart(create_feature_importance_plot(), use_container_width=True)
    
    st.markdown("---")
    with st.expander("Model Architecture & Training Details"):
        st.markdown("""
        **Pipeline Structure:**
        1. `StandardScaler`: Normalizes PCA features and Amount.
        2. `RandomForestClassifier`:
           - `n_estimators`: 100
           - `class_weight`: balanced
           - `max_depth`: 10
           - `random_state`: 42
           
        **Training Data:** Kaggle Credit Card Fraud Dataset (European cardholders, Sept 2013).
        Highly unbalanced (0.172% fraud). `class_weight="balanced"` was utilized to penalize false negatives heavily.
        """)

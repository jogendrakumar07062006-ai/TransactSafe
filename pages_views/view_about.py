# pages_views/view_about.py

import streamlit as st

def render():
    st.title("ℹ️ About TransactSafe")
    st.markdown("""
    **TransactSafe** is a next-generation SOC (Security Operations Center) dashboard designed for fintech and banking environments.
    
    ### Architecture
    1. **Machine Learning Core**: A Random Forest classifier trained on historic transaction data to identify complex, non-linear fraud patterns.
    2. **Heuristic Rule Engine**: Deterministic overrides for known attack vectors (e.g., late-night micro-transactions).
    3. **AI Analyst (LLM Integration)**: Utilizes Groq/Gemini to translate raw model output and rule flags into human-readable explanations, reducing analyst triage time.
    
    ### Technologies
    - **Frontend**: Streamlit, Plotly, custom CSS (Glassmorphism, Dark UI)
    - **Backend Engine**: scikit-learn, joblib, pandas
    - **LLM Provider**: Groq API
    """)

# dashboard.py

import streamlit as st

# Configure Streamlit page at the very top
st.set_page_config(
    page_title="TransactSafe SOC", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

from styles import apply_custom_styles
from pages_views import view_dashboard, view_analysis, view_batch, view_model, view_about

def main():
    apply_custom_styles()
    
    # Sidebar Navigation
    with st.sidebar:
        st.title("🛡️ TransactSafe")
        st.markdown("**Enterprise Fraud Risk Platform**")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "🔍 Transaction Analysis", "📁 Batch Analysis", "🧠 Model Performance", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### System Status")
        st.success("🧠 ML Engine: **Active**")
        st.success("🤖 AI Analyst: **Ready**")
        st.info("🔌 API Status: **Online**")
        
    # Page Routing
    if page == "📊 Dashboard":
        view_dashboard.render()
    elif page == "🔍 Transaction Analysis":
        view_analysis.render()
    elif page == "📁 Batch Analysis":
        view_batch.render()
    elif page == "🧠 Model Performance":
        view_model.render()
    elif page == "ℹ️ About":
        view_about.render()

if __name__ == "__main__":
    main()

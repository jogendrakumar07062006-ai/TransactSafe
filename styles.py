# styles.py

import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Modern Dark Theme - SOC / Fintech Dashboard */
        :root {
            --bg-color: #0B0F19;
            --surface-color: #111827;
            --surface-light: #1E293B;
            --border-color: #334155;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --accent-green: #10B981;
            --accent-yellow: #F59E0B;
            --accent-red: #EF4444;
            --accent-brand: #6366F1;
        }
        
        /* Global Backgrounds */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-primary);
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: var(--surface-color);
            border-right: 1px solid var(--border-color);
        }
        
        /* Header styling */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Metric Cards */
        div[data-testid="metric-container"] {
            background: linear-gradient(145deg, var(--surface-color), var(--surface-light));
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            border-color: var(--accent-brand);
            box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
        }
        
        /* Hide metric label default color, apply custom */
        div[data-testid="stMetricLabel"] > div {
            color: var(--text-secondary) !important;
            font-weight: 500;
            font-size: 0.9rem;
        }
        div[data-testid="stMetricValue"] > div {
            color: var(--text-primary) !important;
            font-weight: 700;
            font-size: 1.8rem;
        }
        
        /* Styled Containers */
        .css-1r6slb0.e1tzin5v2 {
            background-color: var(--surface-color);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--border-color);
        }

        /* Expander overrides */
        .streamlit-expanderHeader {
            background-color: var(--surface-light);
            border-radius: 8px;
            color: var(--text-primary);
        }
        
        /* Buttons */
        .stButton > button {
            background-color: var(--accent-brand);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background-color: #4F46E5;
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
            color: white;
            border: none;
        }

        /* Custom Risk Badges */
        .risk-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .risk-low {
            background-color: rgba(16, 185, 129, 0.1);
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }
        .risk-medium {
            background-color: rgba(245, 158, 11, 0.1);
            color: var(--accent-yellow);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }
        .risk-high {
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--accent-red);
            border: 1px solid rgba(239, 68, 68, 0.2);
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
        }
        .status-dot {
            height: 8px;
            width: 8px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 6px;
        }
        .status-dot.green { background-color: var(--accent-green); }
        .status-dot.yellow { background-color: var(--accent-yellow); }
        .status-dot.red { background-color: var(--accent-red); }

        /* LLM Explanation Card */
        .ai-analyst-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
            border-left: 4px solid var(--accent-brand);
            border-radius: 8px;
            padding: 16px;
            margin-top: 16px;
            color: var(--text-primary);
        }
        .ai-analyst-header {
            display: flex;
            align-items: center;
            font-weight: 600;
            color: var(--accent-brand);
            margin-bottom: 8px;
            font-size: 1rem;
        }
        
        /* Table overrides */
        [data-testid="stTable"], [data-testid="stDataFrame"] {
            background-color: var(--surface-color);
            border-radius: 8px;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background-color: var(--surface-light);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

def risk_badge_html(tier: str) -> str:
    tier = tier.lower()
    if tier == "high":
        return '<div class="risk-badge risk-high"><span class="status-dot red"></span>HIGH FRAUD RISK</div>'
    elif tier == "medium":
        return '<div class="risk-badge risk-medium"><span class="status-dot yellow"></span>MEDIUM RISK</div>'
    else:
        return '<div class="risk-badge risk-low"><span class="status-dot green"></span>GENUINE / LOW RISK</div>'

def ai_card_html(explanation_text: str, provider: str, latency: float) -> str:
    prov_text = provider if provider else "Fallback/Heuristic"
    return f"""
    <div class="ai-analyst-card">
        <div class="ai-analyst-header">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
                <path d="M12 2a2 2 0 0 1 2 2c-.11.66-.54 1.25-1.12 1.63L9.5 8 8 11h8l1.5-3-3.38-2.37A2.04 2.04 0 0 1 12 2Z"></path>
                <path d="m14 11 1 9H9l1-9"></path>
                <path d="M4 8h16"></path>
                <path d="M4 14h16"></path>
            </svg>
            AI Security Analyst
        </div>
        <div style="font-size: 0.95rem; line-height: 1.5;">{explanation_text}</div>
        <div style="margin-top: 12px; font-size: 0.75rem; color: var(--text-secondary); display: flex; gap: 16px;">
            <span><strong>Model:</strong> {prov_text}</span>
            <span><strong>Latency:</strong> {latency} ms</span>
        </div>
    </div>
    """

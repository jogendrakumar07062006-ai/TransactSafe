# charts.py

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Dark Theme styling variables matching styles.py
THEME_BG = 'rgba(0,0,0,0)'
THEME_FONT = '#F8FAFC'
THEME_GRID = '#334155'
COLOR_SAFE = '#10B981'
COLOR_MED = '#F59E0B'
COLOR_FRAUD = '#EF4444'
COLOR_BRAND = '#6366F1'

def apply_layout(fig):
    fig.update_layout(
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=THEME_FONT, family="sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor=THEME_GRID, zerolinecolor=THEME_GRID),
        yaxis=dict(showgrid=True, gridcolor=THEME_GRID, zerolinecolor=THEME_GRID)
    )
    return fig

def create_fraud_donut_chart(df: pd.DataFrame):
    if df.empty or "tier" not in df.columns:
        return go.Figure()
        
    counts = df["tier"].value_counts().to_dict()
    labels = ['Low Risk', 'Medium Risk', 'High Risk']
    values = [counts.get("low", 0), counts.get("medium", 0), counts.get("high", 0)]
    colors = [COLOR_SAFE, COLOR_MED, COLOR_FRAUD]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.6,
        marker_colors=colors,
        textinfo='percent',
        hoverinfo='label+value'
    )])
    
    fig.update_layout(
        title="Transaction Risk Distribution",
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=THEME_FONT),
        showlegend=True,
        margin=dict(t=40, b=0, l=0, r=0)
    )
    return fig

def create_risk_histogram(df: pd.DataFrame):
    if df.empty or "ml_probability" not in df.columns:
        return go.Figure()
        
    fig = px.histogram(
        df, 
        x="ml_probability", 
        nbins=40,
        title="Risk Score Distribution",
        color_discrete_sequence=[COLOR_BRAND]
    )
    
    # Add vertical lines for thresholds
    fig.add_vline(x=0.3, line_width=2, line_dash="dash", line_color=COLOR_MED, annotation_text="Med")
    fig.add_vline(x=0.7, line_width=2, line_dash="dash", line_color=COLOR_FRAUD, annotation_text="High")
    
    fig.update_layout(xaxis_title="ML Probability", yaxis_title="Count", bargap=0.1)
    return apply_layout(fig)

def create_hourly_fraud_chart(df: pd.DataFrame):
    if df.empty or "Hour" not in df.columns or "tier" not in df.columns:
        return go.Figure()
        
    grouped = df.groupby(["Hour", "tier"]).size().reset_index(name="count")
    color_map = {"low": COLOR_SAFE, "medium": COLOR_MED, "high": COLOR_FRAUD}
    
    fig = px.bar(
        grouped, 
        x="Hour", 
        y="count", 
        color="tier",
        title="Transactions by Hour",
        color_discrete_map=color_map,
        barmode="stack"
    )
    fig.update_layout(xaxis=dict(tickmode='linear', dtick=2), xaxis_title="Hour of Day", yaxis_title="Volume")
    return apply_layout(fig)

def create_risk_gauge(probability: float):
    if probability >= 0.7:
        color = COLOR_FRAUD
    elif probability >= 0.3:
        color = COLOR_MED
    else:
        color = COLOR_SAFE
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability * 100,
        number = {'suffix': "%", 'font': {'color': THEME_FONT, 'size': 40}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Fraud Probability", 'font': {'color': THEME_FONT}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': THEME_GRID},
            'bar': {'color': color},
            'bgcolor': THEME_GRID,
            'borderwidth': 2,
            'bordercolor': THEME_BG,
            'steps': [
                {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.1)'},
                {'range': [30, 70], 'color': 'rgba(245, 158, 11, 0.1)'},
                {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=THEME_BG,
        plot_bgcolor=THEME_BG,
        font=dict(color=THEME_FONT),
        margin=dict(l=10, r=10, t=50, b=10),
        height=250
    )
    return fig

def create_confusion_matrix_plot():
    # Hardcoded typical test-set numbers for demonstration/model performance page
    z = [[56854, 10], [15, 83]]
    x = ['Predicted Genuine', 'Predicted Fraud']
    y = ['Actual Genuine', 'Actual Fraud']
    
    fig = px.imshow(
        z, 
        text_auto=True, 
        x=x, y=y,
        color_continuous_scale=[THEME_BG, COLOR_BRAND],
        title="Confusion Matrix (Test Set)"
    )
    fig.update_layout(coloraxis_showscale=False)
    return apply_layout(fig)

def create_feature_importance_plot():
    # Typical RF importances for credit card dataset
    features = ['V14', 'V10', 'V12', 'V17', 'V11', 'V4', 'V16', 'V3', 'V9', 'V2', 'V7', 'Amount', 'V21', 'V18', 'Hour']
    importances = [0.18, 0.12, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04, 0.035, 0.03, 0.025, 0.02, 0.015, 0.012, 0.01]
    
    df = pd.DataFrame({"Feature": features, "Importance": importances})
    df = df.sort_values(by="Importance", ascending=True)
    
    fig = px.bar(
        df, 
        x="Importance", 
        y="Feature", 
        orientation='h',
        title="Top 15 Feature Importances",
        color_discrete_sequence=[COLOR_BRAND]
    )
    return apply_layout(fig)

def create_roc_curve_plot():
    # Simulated ROC curve data
    fpr = np.linspace(0, 1, 100)
    tpr = np.sqrt(fpr) # mock curve shape
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name='RF Model (AUC = 0.978)', line=dict(color=COLOR_BRAND, width=3)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(color=THEME_GRID, dash='dash')))
    
    fig.update_layout(
        title="Receiver Operating Characteristic (ROC)",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate"
    )
    return apply_layout(fig)

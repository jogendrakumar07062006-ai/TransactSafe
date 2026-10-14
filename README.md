🛡️ TransactSafe

AI-Powered Transaction Fraud Risk & SOC Dashboard

TransactSafe is a fraud-risk analysis platform that combines machine-learning inference, heuristic rules, and AI-generated analyst explanations to help identify and investigate potentially fraudulent financial transactions.

The dashboardAntigravity branch expands the project into a SOC-style Streamlit interface with dedicated views for transaction analysis, batch analysis, model performance, and system information. It also adds reusable charting, styling, and dashboard utility modules.

Branch documented: dashboardAntigravity

✨ Features

🤖 ML Fraud Detection

Uses the trained fraud-detection model stored in models/fraud_model.joblib.

Produces a fraud probability for every analyzed transaction.

Supports the transaction feature set used by the project's PCA-based fraud model.

🧩 Rule-Based Risk Analysis

TransactSafe complements the ML score with lightweight heuristics:

Low Amount Flag — transactions below $5.00

Night Hour Flag — transactions between 01:00 and 05:00

These signals are combined with the ML probability to determine the final risk tier.

🎯 Risk Classification

Transactions are categorized into:

Tier

ML Probability

🔴 High

>= 0.70

🟡 Medium

>= 0.30

🟢 Low

< 0.30

Additional rule-based signals can influence the final tier.

🧠 AI Analyst

Risky transactions can receive a natural-language explanation from the configured LLM provider.

The dashboard displays:

Risk explanation

AI provider

LLM latency

Triggered heuristic rules

ML probability

This provides an analyst-friendly interpretation instead of exposing only a numerical model score.

📊 SOC Dashboard

The new dashboard provides a centralized view of processed transactions, including:

Total transactions

High-risk/fraudulent transactions

Fraud rate

Average risk score

Average LLM latency

Fraud distribution

Hourly fraud activity

Risk-score distribution

Recent transaction feed

The dashboard uses Plotly-based visualizations and a custom dark SOC/fintech theme.

🔍 Single Transaction Analysis

The Transaction Analysis page allows analysts to:

Select synthetic transaction presets:

Legitimate

Night Micro-transaction

High-Value Fraud

Manual

Enter transaction amount and hour.

Enter V1–V28 PCA features.

Run ML inference.

Evaluate rules.

Assign a risk tier.

Request an AI explanation.

View a risk gauge.

Save the transaction to the application store.

📁 Batch Analysis

The dashboard includes a dedicated Batch Analysis view for analyzing transaction datasets in bulk.

🧠 Model Performance

The dashboard includes a Model Performance view for presenting model-related information and evaluation metrics.

🎨 Custom UI

The dashboardAntigravity branch introduces:

Dark SOC/fintech visual theme

Custom metric cards

Risk badges

Status indicators

AI analyst cards

Styled tables

Custom buttons and containers

Responsive Streamlit layout

🏗️ Architecture

                         ┌──────────────────────────┐
                         │       Streamlit UI       │
                         │     TransactSafe SOC     │
                         └────────────┬─────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
     ┌───────────────┐       ┌────────────────┐       ┌─────────────────┐
     │  Dashboard    │       │  Transaction   │       │ Batch Analysis  │
     │  View         │       │  Analysis      │       │ View            │
     └───────┬───────┘       └───────┬────────┘       └────────┬────────┘
             │                       │                         │
             └───────────────────────┼─────────────────────────┘
                                     ▼
                           ┌───────────────────┐
                           │   Fraud Scoring   │
                           └─────────┬─────────┘
                                     │
                     ┌───────────────┼────────────────┐
                     ▼               ▼                ▼
              ┌────────────┐  ┌────────────┐  ┌──────────────┐
              │ ML Model   │  │ Rule Engine │  │ AI Analyst   │
              │ Probability│  │ Heuristics │  │ Explanation  │
              └──────┬─────┘  └──────┬─────┘  └──────┬───────┘
                     │               │                │
                     └───────────────┼────────────────┘
                                     ▼
                           ┌───────────────────┐
                           │  Risk Tier +      │
                           │  Analysis Record  │
                           └─────────┬─────────┘
                                     ▼
                           ┌───────────────────┐
                           │ In-Memory Storage │
                           └───────────────────┘

🖥️ Dashboard Navigation

The Streamlit application provides five main sections:

📊 Dashboard

The global SOC overview.

It calculates and displays metrics such as:

Total transactions

High-risk transactions

Fraud rate

Average risk score

Average LLM latency

It also renders:

Fraud donut chart

Hourly fraud chart

Risk histogram

Recent transaction feed

The dashboard reads scored transactions from the application's storage layer.

🔍 Transaction Analysis

Analyze one transaction interactively.

The interface supports both presets and manual input:

Legitimate
Night Micro-transaction
High-Value Fraud
Manual

Advanced PCA features V3–V28 are grouped into an expandable section.

After analysis, the UI shows:

Risk Gauge
    ↓
Risk Tier
    ↓
Triggered Rules
    ↓
AI Analyst Explanation

📁 Batch Analysis

Analyze multiple transactions from a dataset rather than entering them individually.

This is intended for higher-volume fraud investigation workflows.

🧠 Model Performance

Provides a dedicated location for viewing model performance information and evaluation results.

ℹ️ About

Provides information about the TransactSafe application and its architecture.

📈 Visualizations

The dashboard contains reusable chart functions in charts.py.

Current visualization components include:

Fraud Donut Chart

Hourly Fraud Chart

Risk Histogram

Risk Gauge

These charts are separated from the page logic so they can be reused across dashboard views.

📁 Project Structure

The dashboardAntigravity branch currently has the following major structure:

transactsafe/
│
├── app/
│   ├── config.py
│   ├── llm_explain.py
│   ├── main.py
│   ├── model_utils.py
│   ├── rules.py
│   ├── schemas.py
│   └── storage.py
│
├── data/
│   └── sample_transactions.csv
│
├── models/
│   └── fraud_model.joblib
│
├── notebooks/
│   └── explore_and_train.ipynb
│
├── pages_views/
│   ├── view_about.py
│   ├── view_analysis.py
│   ├── view_batch.py
│   ├── view_dashboard.py
│   └── view_model.py
│
├── charts.py
├── dashboard.py
├── styles.py
├── utils.py
├── requirements.txt
├── NOTES.md
└── README.md

Module Responsibilities

File / Directory

Purpose

app/

Core fraud-scoring backend logic

app/main.py

FastAPI application/API

app/model_utils.py

ML model loading and inference

app/rules.py

Heuristic risk rules

app/llm_explain.py

LLM-based explanations

app/storage.py

Transaction storage

app/schemas.py

API/data schemas

app/config.py

Application configuration

pages_views/

Streamlit page implementations

charts.py

Plotly chart generation

styles.py

Custom Streamlit styling

utils.py

Dashboard scoring/preset utilities

dashboard.py

Streamlit application entry point

data/

Sample transaction data

models/

Serialized fraud model

notebooks/

Model exploration/training work

🔄 Transaction Analysis Flow

A transaction follows this general pipeline:

Transaction Input
       │
       ▼
Feature Preparation
       │
       ▼
ML Fraud Probability
       │
       ├───────────────┐
       │               │
       ▼               ▼
 Rule Evaluation    Risk Scoring
       │               │
       └───────┬───────┘
               ▼
          Risk Tier
               │
               ▼
       AI Analyst Explanation
               │
               ▼
        Save Transaction
               │
               ▼
        Dashboard Metrics

🧮 Risk Rules

Two basic heuristic signals are currently used.

Low Amount

Amount < $5.00

Night Hour

01:00 <= Hour <= 05:00

The dashboard explicitly displays these signals after a transaction is analyzed.

🧠 ML Features

The model works with the transaction representation containing:

Time / Hour
Amount
V1 ... V28

The V1–V28 features represent the PCA-transformed transaction attributes used by the fraud model.

The dashboard exposes:

V1

V2

directly in the primary form and places:

V3–V28

inside an expandable Advanced PCA Features section.

⚙️ Installation

1. Clone the repository

git clone https://github.com/jogendrakumar07062006/Transactsafe.git
cd transactsafe

2. Checkout the dashboard branch

git checkout dashboardAntigravity

3. Create a virtual environment

python3 -m venv .venv
source .venv/bin/activate

On Windows:

.venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

🔐 Environment Variables

If the AI explanation functionality requires an API key, create a .env file in the project root and configure the key expected by the application.

For example:

GROQ_API_KEY=your_groq_api_key

Never commit API keys or other secrets to Git.

▶️ Running TransactSafe

Start the FastAPI backend

From the repository root:

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

Start the Streamlit SOC Dashboard

In another terminal:

streamlit run dashboard.py

The Streamlit interface will open in your browser.

🧪 Using the Dashboard

Quick demo

Start the backend.

Start Streamlit.

Open Transaction Analysis.

Select one of the preset profiles.

Click Analyze Transaction.

Review:

ML probability

Risk gauge

Risk tier

Triggered rules

AI explanation

Open Dashboard to see the transaction reflected in the SOC metrics.

For batch workflows, use Batch Analysis.

💾 Data Storage

The current application uses an in-memory transaction store.

This means:

Application running
      ↓
Transactions stored
      ↓
Dashboard reads transactions
      ↓
Application restart
      ↓
Stored transaction history is lost

For a production deployment, persistent storage such as PostgreSQL would be more appropriate.

🧪 Model Development

The repository contains:

notebooks/explore_and_train.ipynb

This notebook is intended for model exploration and training.

The resulting serialized model is stored at:

models/fraud_model.joblib

Keeping the model artifact separate from the application code allows the inference layer to load a trained model without retraining every time the application starts.

🛠️ Tech Stack

Layer

Technology

Language

Python

Dashboard

Streamlit

API

FastAPI

Data Validation

Pydantic

ML

scikit-learn

Model Serialization

joblib

Data Processing

pandas / NumPy

Visualization

Plotly

AI Explanation

Groq LLM API

Configuration

python-dotenv

UI Styling

Custom CSS

🔒 Security Considerations

TransactSafe is currently a project/prototype implementation.

Before using it for real financial transactions, consider adding:

API authentication

Authorization / role-based access

HTTPS/TLS

Persistent encrypted storage

Audit logging

Secret management

Rate limiting

Input validation hardening

Model monitoring

Model drift detection

LLM prompt-injection protections

PII/data minimization

Secure deployment configuration

The application should not be treated as a standalone system for automatically approving or declining real financial transactions.

🚧 Current Limitations

Transaction records are currently stored in memory.

Dashboard and API deployment are primarily configured for local development.

The fraud model is a pre-trained artifact and requires the expected feature representation.

LLM availability depends on the configured provider/API credentials.

The current rule engine contains only a small set of heuristic checks.

Production-grade authentication and authorization are not implemented.

Model monitoring and automated retraining are not yet included.

The dashboard is primarily an analyst interface rather than a complete transaction-processing platform.

🔮 Future Improvements

Potential extensions include:

Infrastructure

PostgreSQL transaction storage

Redis caching

Docker / Docker Compose

Production deployment

CI/CD pipeline

Fraud Detection

Ensemble models

Real-time feature engineering

Model drift monitoring

Automated retraining

Precision/recall optimization

Explainable ML using SHAP

SOC Capabilities

Analyst authentication

Case management

Transaction investigation workflow

Alert prioritization

Analyst feedback

Audit trails

Real-time alerting

AI

More reliable structured explanations

LLM cost tracking

Prompt versioning

AI response evaluation

Retrieval-augmented fraud investigation

Guardrails against prompt injection

📌 Why TransactSafe?

Traditional fraud detection often produces a score or binary decision.

TransactSafe combines multiple signals:

Machine Learning
       +
Heuristic Rules
       +
AI Explanation
       +
SOC Dashboard
       =
Analyst-Oriented Fraud Risk Platform

The goal is not simply to say "this transaction is suspicious", but to give an analyst a structured view of how risky it appears, which rules were triggered, and why the transaction deserves attention.

👨‍💻 Author

Jogendra Kumar

GitHub: https://github.com/jogendrakumar07062006

Repository:

https://github.com/jogendrakumar07062006/Transactsafe

⚠️ Disclaimer

TransactSafe is a research/educational project and should not be considered a production-ready financial fraud prevention system.

Fraud predictions can contain false positives and false negatives. Any real-world financial decision should incorporate appropriate validation, monitoring, security controls, and human oversight.

# app/storage.py

scored_transactions = []

def save_transaction(record: dict):
    scored_transactions.append(record)

def get_all_transactions():
    return scored_transactions

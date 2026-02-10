import pandas as pd
import numpy as np

def calculate_conversion_score(row):
    debt = row.get("debt_amount", 0) or 0
    income = row.get("income_monthly", 0) or 0

    # Basic financial stress ratio
    ratio = 0
    if income > 0:
        ratio = debt / (income * 12)

    # Scoring logic
    score = 0

    if debt >= 25000:
        score += 40
    elif debt >= 15000:
        score += 25
    elif debt >= 8000:
        score += 15

    if ratio > 0.8:
        score += 30
    elif ratio > 0.5:
        score += 20
    elif ratio > 0.3:
        score += 10

    if income >= 4000:
        score += 20
    else:
        score += 10

    return min(score, 100)

def add_ml_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["conversion_score"] = df.apply(calculate_conversion_score, axis=1)
    return df

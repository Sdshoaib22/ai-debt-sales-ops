import pandas as pd

def score_priority(row) -> str:
    debt = row.get("debt_amount")

    # Simple scoring rules (we upgrade later to ML model)
    if debt is not None and debt >= 20000:
        return "HOT"
    if debt is not None and debt >= 10000:
        return "WARM"
    return "COLD"

def add_priority(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["priority"] = df.apply(score_priority, axis=1)
    return df

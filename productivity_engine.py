from datetime import datetime

def add_productivity_metrics(df):
    df = df.copy()

    if "created_at" not in df.columns:
        df["created_at"] = datetime.now()

    df["days_open"] = (
        datetime.now() - df["created_at"]
    ).dt.days

    df["escalation_flag"] = (
        (df["priority"] == "HOT") & 
        (df["status"] == "Open") & 
        (df["days_open"] > 2)
    )

    return df

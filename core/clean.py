import re
import pandas as pd

def clean_phone(x):
    if pd.isna(x):
        return None
    s = re.sub(r"\D", "", str(x))
    if len(s) == 11 and s.startswith("1"):
        s = s[1:]
    return s if len(s) == 10 else None

def clean_email(x):
    if pd.isna(x):
        return None
    s = str(x).strip().lower()
    return s if "@" in s and "." in s else None

def clean_money(x):
    if pd.isna(x):
        return None
    s = str(x).replace("$", "").replace(",", "").strip()
    try:
        return float(s)
    except:
        return None

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "phone" in df.columns:
        df["phone"] = df["phone"].apply(clean_phone)

    if "email" in df.columns:
        df["email"] = df["email"].apply(clean_email)

    if "debt" in df.columns and "debt_amount" not in df.columns:
        df["debt_amount"] = df["debt"].apply(clean_money)

    if "debt_amount" in df.columns:
        df["debt_amount"] = df["debt_amount"].apply(clean_money)

    if "income" in df.columns and "income_monthly" not in df.columns:
        df["income_monthly"] = df["income"].apply(clean_money)

    if "income_monthly" in df.columns:
        df["income_monthly"] = df["income_monthly"].apply(clean_money)

    for col in ["first_name", "last_name", "city", "province", "postal_code", "source"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": None, "None": None})

    return df

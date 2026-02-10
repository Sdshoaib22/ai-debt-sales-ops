import pandas as pd
from rapidfuzz import fuzz

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Exact dedupe on email
    if "email" in df.columns:
        df = df.drop_duplicates(subset=["email"], keep="first")

    # Exact dedupe on phone
    if "phone" in df.columns:
        df = df.drop_duplicates(subset=["phone"], keep="first")

    # Fuzzy dedupe using first_name + last_name + city
    if all(col in df.columns for col in ["first_name", "last_name", "city"]):
        kept_rows = []
        seen_keys = []

        for _, row in df.iterrows():
            key = f"{row.get('first_name','')} {row.get('last_name','')}|{row.get('city','')}"
            is_duplicate = False

            for existing in seen_keys:
                if fuzz.token_sort_ratio(key, existing) >= 92:
                    is_duplicate = True
                    break

            if not is_duplicate:
                seen_keys.append(key)
                kept_rows.append(row)

        df = pd.DataFrame(kept_rows)

    return df.reset_index(drop=True)

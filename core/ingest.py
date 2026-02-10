import pandas as pd

def load_excel(file_bytes) -> pd.DataFrame:
    df = pd.read_excel(file_bytes, engine="openpyxl")
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df

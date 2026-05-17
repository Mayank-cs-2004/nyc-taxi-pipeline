import pandas as pd

def extract(filepath: str) -> pd.DataFrame:
    print(f"[extract] Loading {filepath}")
    df = pd.read_parquet(filepath)
    print(f"[extract] Loaded {len(df):,} rows, {len(df.columns)} columns")
    return df

import pandas as pd
from pathlib import Path

def load(df: pd.DataFrame, output_dir: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # save clean data
    clean_path = output_dir / "yellow_taxi_clean.parquet"
    df.to_parquet(clean_path, index=False)
    print(f"[load] Saved clean data → {clean_path}")

    # save a summary
    summary = {
        "total_trips": len(df),
        "avg_fare": round(df["fare_amount"].mean(), 2),
        "avg_distance_miles": round(df["trip_distance"].mean(), 2),
        "avg_duration_minutes": round(df["trip_duration_minutes"].mean(), 2),
        "busiest_hour": int(df["pickup_hour"].mode()[0]),
        "busiest_day": df["pickup_day_of_week"].mode()[0],
    }

    summary_df = pd.DataFrame([summary])
    summary_path = output_dir / "summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"[load] Saved summary → {summary_path}")
    print(f"\n{'='*40}")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print('='*40)

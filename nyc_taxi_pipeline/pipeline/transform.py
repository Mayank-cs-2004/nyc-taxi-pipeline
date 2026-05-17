import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:
    print("[transform] Cleaning data...")
    original_count = len(df)

    # fix types
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    # drop bad rows
    df = df[df["trip_distance"] > 0]
    df = df[df["fare_amount"] > 0]
    df = df[df["passenger_count"] > 0]
    df = df.dropna(subset=["PULocationID", "DOLocationID"])

    # add useful columns
    df["trip_duration_minutes"] = (
        (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"])
        .dt.total_seconds() / 60
    )
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
    df["pickup_day_of_week"] = df["tpep_pickup_datetime"].dt.day_name()
    df["cost_per_mile"] = df["fare_amount"] / df["trip_distance"]

    # drop absurd trip durations (under 1 min or over 5 hours)
    df = df[(df["trip_duration_minutes"] >= 1) & (df["trip_duration_minutes"] <= 300)]

    removed = original_count - len(df)
    print(f"[transform] Removed {removed:,} bad rows. {len(df):,} rows remaining.")
    return df

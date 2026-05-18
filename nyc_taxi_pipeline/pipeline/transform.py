from pyspark.sql.functions import (
    col, to_timestamp, hour, dayofweek, dayname, 
    round as spark_round, datediff, when
)

def transform(df):
    """Clean and enrich data using Spark"""
    print("[transform] Cleaning data with Spark...")
    original_count = df.count()
    
    # Fix types
    df = df.withColumn("tpep_pickup_datetime", to_timestamp("tpep_pickup_datetime"))
    df = df.withColumn("tpep_dropoff_datetime", to_timestamp("tpep_dropoff_datetime"))
    
    # Filter bad rows
    df = df.filter(col("trip_distance") > 0)
    df = df.filter(col("fare_amount") > 0)
    df = df.filter(col("passenger_count") > 0)
    df = df.filter(col("PULocationID").isNotNull())
    df = df.filter(col("DOLocationID").isNotNull())
    
    # Add useful columns
    df = df.withColumn(
        "trip_duration_minutes",
        spark_round(
            (datediff(col("tpep_dropoff_datetime"), col("tpep_pickup_datetime")) * 24 * 60 +
             (col("tpep_dropoff_datetime").cast("long") - col("tpep_pickup_datetime").cast("long")) / 60) 
            / 60, 2
        )
    )
    df = df.withColumn("pickup_hour", hour(col("tpep_pickup_datetime")))
    df = df.withColumn("pickup_day_of_week", dayname(col("tpep_pickup_datetime")))
    df = df.withColumn("cost_per_mile", spark_round(col("fare_amount") / col("trip_distance"), 2))
    
    # Filter absurd durations
    df = df.filter((col("trip_duration_minutes") >= 1) & (col("trip_duration_minutes") <= 300))
    
    final_count = df.count()
    removed = original_count - final_count
    print(f"[transform] Removed {removed:,} bad rows. {final_count:,} rows remaining.")
    
    return df

import pandas as pd
import psycopg2
from config import DB_CONFIG

def load(df: pd.DataFrame):
    """Write cleaned data to Postgres instead of parquet"""
    print("[load] Connecting to Postgres...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("[load] Connected!")
        
        # Drop table if it exists (fresh start each run)
        cursor.execute("DROP TABLE IF EXISTS taxi_trips CASCADE;")
        print("[load] Creating table...")
        
        # Create table
        cursor.execute("""
            CREATE TABLE taxi_trips (
                trip_id SERIAL PRIMARY KEY,
                vendor_id INTEGER,
                tpep_pickup_datetime TIMESTAMP,
                tpep_dropoff_datetime TIMESTAMP,
                passenger_count INTEGER,
                trip_distance NUMERIC,
                pickup_longitude NUMERIC,
                pickup_latitude NUMERIC,
                dropoff_longitude NUMERIC,
                dropoff_latitude NUMERIC,
                fare_amount NUMERIC,
                extra NUMERIC,
                mta_tax NUMERIC,
                tip_amount NUMERIC,
                tolls_amount NUMERIC,
                total_amount NUMERIC,
                payment_type INTEGER,
                trip_duration_minutes INTEGER,
                pickup_hour INTEGER,
                pickup_day_of_week VARCHAR(10),
                cost_per_mile NUMERIC,
                PULocationID INTEGER,
                DOLocationID INTEGER
            );
        """)
        print("[load] Table created!")
        
        # Insert data
        print(f"[load] Inserting {len(df):,} rows...")
        for idx, row in df.iterrows():
            cursor.execute("""
                INSERT INTO taxi_trips (
                    vendor_id, tpep_pickup_datetime, tpep_dropoff_datetime,
                    passenger_count, trip_distance, pickup_longitude, pickup_latitude,
                    dropoff_longitude, dropoff_latitude, fare_amount, extra, mta_tax,
                    tip_amount, tolls_amount, total_amount, payment_type,
                    trip_duration_minutes, pickup_hour, pickup_day_of_week, cost_per_mile,
                    PULocationID, DOLocationID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row.get('VendorID'), row['tpep_pickup_datetime'], row['tpep_dropoff_datetime'],
                row['passenger_count'], row['trip_distance'], row.get('pickup_longitude'),
                row.get('pickup_latitude'), row.get('dropoff_longitude'), row.get('dropoff_latitude'),
                row['fare_amount'], row.get('extra'), row.get('mta_tax'),
                row.get('tip_amount'), row.get('tolls_amount'), row.get('total_amount'),
                row.get('payment_type'), row['trip_duration_minutes'], row['pickup_hour'],
                row['pickup_day_of_week'], row['cost_per_mile'],
                row['PULocationID'], row['DOLocationID']
            ))
        
        conn.commit()
        print(f"[load] ✅ {len(df):,} rows inserted!")
        
        # Query summary stats from database
        cursor.execute("SELECT COUNT(*) FROM taxi_trips;")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(fare_amount) FROM taxi_trips;")
        avg_fare = round(cursor.fetchone()[0], 2)
        
        cursor.execute("SELECT AVG(trip_distance) FROM taxi_trips;")
        avg_distance = round(cursor.fetchone()[0], 2)
        
        cursor.execute("SELECT AVG(trip_duration_minutes) FROM taxi_trips;")
        avg_duration = round(cursor.fetchone()[0], 2)
        
        print(f"\n{'='*40}")
        print(f"  Total trips: {total:,}")
        print(f"  Avg fare: ${avg_fare}")
        print(f"  Avg distance: {avg_distance} miles")
        print(f"  Avg duration: {avg_duration} minutes")
        print('='*40)
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"[load] ❌ Database error: {e}")
        raise

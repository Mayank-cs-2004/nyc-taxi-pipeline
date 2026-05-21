from config import DB_CONFIG

def load(df):
    """Write Spark DataFrame directly to Postgres using JDBC"""
    print("[load] Writing to Postgres via JDBC...")
    
    # Create raw schema first
    import psycopg2
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    cursor.execute("DROP TABLE IF EXISTS raw.taxi_trips_raw CASCADE;")
    conn.commit()
    conn.close()
    print("[load] Raw schema ready!")
    
    # Write Spark DataFrame directly to Postgres
    df.write \
        .format("jdbc") \
        .mode("overwrite") \
        .option("url", f"jdbc:postgresql://{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}") \
        .option("dbtable", "raw.taxi_trips_raw") \
        .option("user", DB_CONFIG['user']) \
        .option("password", DB_CONFIG['password']) \
        .option("driver", "org.postgresql.Driver") \
        .save()
    
    print(f"[load] ✅ Data written to raw.taxi_trips_raw!")

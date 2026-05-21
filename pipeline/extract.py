from pyspark.sql import SparkSession

def extract(filepath: str):
    """Load parquet file as Spark DataFrame"""
    spark = SparkSession.builder \
        .appName("nyc_taxi_pipeline") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.1") \
        .getOrCreate()
    
    print(f"[extract] Loading {filepath} with Spark...")
    df = spark.read.parquet(filepath)
    
    print(f"[extract] Loaded {df.count():,} rows, {len(df.columns)} columns")
    print(f"[extract] Schema:")
    df.printSchema()
    
    return df

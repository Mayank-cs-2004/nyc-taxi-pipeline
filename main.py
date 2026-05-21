from pipeline.extract import extract
from pipeline.validate import validate
from pipeline.load import load
import subprocess
import os

RAW_FILE = "data/raw/yellow_tripdata_2026-01.parquet"

if __name__ == "__main__":
    print("Starting pipeline...\n")

    # Extract & validate with Spark
    df = extract(RAW_FILE)
    validate(df)
    
    # Load RAW data to Postgres
    print("\n[load] Loading raw data to Postgres...")
    load(df)
    
    # Run dbt transformations
    print("\n[dbt] Running dbt transformations...")
    result = subprocess.run(
        ["dbt", "run"],
        cwd="taxi_dbt",
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"[dbt] ❌ dbt failed with return code {result.returncode}")
        raise Exception("dbt run failed")
    else:
        print("[dbt] ✅ Transformations complete!")

    print("\nPipeline complete.")

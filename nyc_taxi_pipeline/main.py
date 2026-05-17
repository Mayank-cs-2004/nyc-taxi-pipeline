from pipeline.extract import extract
from pipeline.validate import validate
from pipeline.transform import transform
from pipeline.load import load

RAW_FILE = "data/raw/yellow_tripdata_2026-01.parquet"
OUTPUT_DIR = "data/processed"

if __name__ == "__main__":
    print("Starting pipeline...\n")

    df = extract(RAW_FILE)
    validate(df)
    df = transform(df)
    load(df, OUTPUT_DIR)

    print("\nPipeline complete.")

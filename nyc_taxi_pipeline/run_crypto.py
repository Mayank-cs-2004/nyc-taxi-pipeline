from pipeline.fetch_crypto import fetch_crypto_data
from pipeline.load_s3 import upload_to_s3
import os

if __name__ == "__main__":
    print("🚀 Starting Crypto API Pipeline...\n")
    
    # 1. Extract
    filepath = fetch_crypto_data()
    
    # 2. Load to S3
    s3_uri = upload_to_s3(filepath)
    
    # 3. Clean up local file (optional, but good practice since it's in the cloud now!)
    os.remove(filepath)
    print(f"\n[cleanup] Removed local file {filepath}")
    
    print("\n✅ Crypto Pipeline complete!")

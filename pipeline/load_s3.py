import boto3
import os

# Your specific bucket name from the screenshot
BUCKET_NAME = "nyc-taxi-pipeline-kuro-2026"

def upload_to_s3(filepath):
    """Uploads a local file to the raw/ folder in S3"""
    print(f"[load_s3] Connecting to AWS S3...")
    
    # boto3 automatically uses the ~/.aws/credentials file we made!
    s3_client = boto3.client('s3')
    
    file_name = os.path.basename(filepath)
    # We organize it into a 'raw/crypto/' folder inside the bucket
    s3_key = f"raw/crypto/{file_name}"
    
    print(f"[load_s3] Uploading {file_name} to s3://{BUCKET_NAME}/{s3_key}...")
    
    try:
        s3_client.upload_file(filepath, BUCKET_NAME, s3_key)
        print(f"[load_s3] ✅ Successfully uploaded to S3!")
        return f"s3://{BUCKET_NAME}/{s3_key}"
    except Exception as e:
        print(f"[load_s3] ❌ Error uploading to S3: {e}")
        raise

if __name__ == "__main__":
    print("Run this via the main pipeline!")

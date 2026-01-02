import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# Create S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)

print(f"Listing all files in bucket: {AWS_STORAGE_BUCKET_NAME}\n")

try:
    # List all objects in bucket
    response = s3_client.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME)
    
    if 'Contents' in response:
        print(f"Found {len(response['Contents'])} files:\n")
        for obj in response['Contents']:
            print(f"  - {obj['Key']} ({obj['Size']} bytes)")
    else:
        print("No files found in bucket!")
        
except Exception as e:
    print(f"Error: {e}")

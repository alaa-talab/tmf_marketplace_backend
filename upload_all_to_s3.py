import boto3
import os
from pathlib import Path
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

print(f"Uploading files to S3 bucket: {AWS_STORAGE_BUCKET_NAME}\n")

# Paths to upload
media_root = Path('media/photos')

uploaded = 0
errors = 0

for folder in ['originals', 'watermarked']:
    folder_path = media_root / folder
    
    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        continue
        
    print(f"\nProcessing {folder}/...")
    
    for file_path in folder_path.glob('*'):
        if file_path.is_file():
            try:
                # S3 key (path in bucket)
                s3_key = f'photos/{folder}/{file_path.name}'
                
                # Upload file
                with open(file_path, 'rb') as f:
                    s3_client.upload_fileobj(f, AWS_STORAGE_BUCKET_NAME, s3_key)
                
                print(f"  ✓ Uploaded: {s3_key}")
                uploaded += 1
                
            except Exception as e:
                print(f"  ✗ Error uploading {file_path.name}: {e}")
                errors += 1

print(f"\n✓ Upload complete!")
print(f"  Uploaded: {uploaded} files")
print(f"  Errors: {errors}")

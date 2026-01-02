from django.core.management.base import BaseCommand
from photos.models import Photo
import boto3
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate local photo files to S3 storage using boto3'

    def handle(self, *args, **options):
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
        )
        
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        
        if not bucket_name:
            self.stdout.write(self.style.ERROR("AWS_STORAGE_BUCKET_NAME not configured!"))
            return
        
        photos = Photo.objects.all()
        total = photos.count()
        
        self.stdout.write(f"Found {total} photos to migrate to S3: {bucket_name}")
        
        migrated = 0
        skipped = 0
        errors = 0
        
        for photo in photos:
            try:
                # Migrate original image
                if photo.original_image:
                    try:
                        # Get local file path
                        local_path = photo.original_image.path
                        
                        if os.path.exists(local_path):
                            # Define S3 key (path in bucket)
                            s3_key = f'photos/originals/{os.path.basename(local_path)}'
                            
                            # Upload to S3
                            with open(local_path, 'rb') as f:
                                s3_client.upload_fileobj(f, bucket_name, s3_key)
                            
                            # Update database with S3 path
                            photo.original_image.name = s3_key
                            self.stdout.write(f"  ✓ Uploaded original: {photo.title} -> {s3_key}")
                        else:
                            self.stdout.write(self.style.WARNING(f"  ! File not found: {local_path}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"  ✗ Error with original: {photo.title} - {str(e)}"))
                        errors += 1
                
                # Migrate watermarked image
                if photo.watermarked_image:
                    try:
                        local_path = photo.watermarked_image.path
                        
                        if os.path.exists(local_path):
                            s3_key = f'photos/watermarked/{os.path.basename(local_path)}'
                            
                            with open(local_path, 'rb') as f:
                                s3_client.upload_fileobj(f, bucket_name, s3_key)
                            
                            photo.watermarked_image.name = s3_key
                            self.stdout.write(f"  ✓ Uploaded watermarked: {photo.title} -> {s3_key}")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"  ✗ Error with watermarked: {photo.title} - {str(e)}"))
                        errors += 1
                
                # Save updated paths
                photo.save(update_fields=['original_image', 'watermarked_image'])
                migrated += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Unexpected error for {photo.title}: {str(e)}"))
                errors += 1
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Migration complete!"))
        self.stdout.write(f"  Migrated: {migrated}")
        self.stdout.write(f"  Skipped: {skipped}")
        self.stdout.write(f"  Errors: {errors}")

import os
import django
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import random
import datetime

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from photos.models import Photo

User = get_user_model()

def verify_image_processing():
    print("--- Starting Image Processing Verification ---")

    # 1. Create Test User (Uploader)
    username = f'test_uploader_{random.randint(1000, 9999)}'
    email = f'{username}@example.com'
    password = 'testpassword123'
    
    try:
        user = User.objects.create_user(username=username, email=email, password=password, role='Uploader')
        print(f"✅ Created Test User: {user.username} (Role: {user.role})")
    except Exception as e:
        print(f"❌ Failed to create user: {e}")
        return

    # 2. Create a High-Res Image (Mocking an upload)
    print("Generating high-resolution test image (2000x2000)...")
    img = Image.new('RGB', (2000, 2000), color = (73, 109, 137))
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_content = ContentFile(img_io.getvalue(), name='test_high_res.jpg')

    # 3. Create Photo Instance
    print("Uploading photo to model...")
    photo = Photo(
        uploader=user,
        title="Verification Test Image",
        description="A high-res image to test watermarking.",
        capture_date=datetime.date.today(),
        original_image=img_content
    )
    
    # Save (Triggers signals/override save method)
    photo.save()
    print("✅ Photo saved.")

    # 4. Verify Watermark Field
    photo.refresh_from_db()
    
    print("\n--- Verification Results ---")
    print(f"Photo ID: {photo.id}")
    print(f"Original Image: {photo.original_image}")
    
    if photo.watermarked_image:
        print(f"✅ Watermarked Image Field Populated: {photo.watermarked_image}")
    else:
        print("❌ Watermarked Image Field is EMPTY!")

    # 5. Print URLs
    print("\n--- File URLs ---")
    try:
        print(f"Original URL:     {photo.original_image.url}")
    except Exception as e:
        print(f"Could not get Original URL: {e}")

    try:
        if photo.watermarked_image:
            print(f"Watermarked URL:  {photo.watermarked_image.url}")
        else:
            print("Watermarked URL:  N/A")
    except Exception as e:
        print(f"Could not get Watermarked URL: {e}")

    print("\n-------------------------------------------")

if __name__ == "__main__":
    verify_image_processing()

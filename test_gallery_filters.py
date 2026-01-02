import os
import django
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import datetime

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from photos.models import Photo
from rest_framework.test import APIRequestFactory, force_authenticate
from photos.views import GalleryView

User = get_user_model()

def test_gallery_filtering():
    print("--- Starting Gallery Filtering Test ---")

    # 1. Setup Data
    # Create Uploader to upload photos
    uploader, _ = User.objects.get_or_create(username='test_uploader_filter', role='Uploader')
    # Create Buyer to view gallery
    buyer, _ = User.objects.get_or_create(username='test_buyer_filter', role='Buyer')

    # Dummy Image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_content = ContentFile(img_io.getvalue(), name='test.jpg')

    # Clear existing photos for clean test or just count new ones? 
    # Let's clean up only the ones we create or assume created_at ordering helps. 
    # Better to create unique titles and check for expected IDs or Titles.
    
    # Photo A: Complete
    photo_a = Photo.objects.create(
        uploader=uploader,
        title="Photo A (Complete)",
        description="Has description",
        capture_date=datetime.date.today(),
        original_image=ContentFile(img_io.getvalue(), name='test_a.jpg')
    )
    print(f"Created Photo A: {photo_a.title} (ID: {photo_a.id})")

    # Photo B: Missing Description
    photo_b = Photo.objects.create(
        uploader=uploader,
        title="Photo B (No Desc)",
        description="",
        capture_date=datetime.date.today(),
        original_image=ContentFile(img_io.getvalue(), name='test_b.jpg')
    )
    print(f"Created Photo B: {photo_b.title} (ID: {photo_b.id})")

    # Photo C: Missing Capture Date
    photo_c = Photo.objects.create(
        uploader=uploader,
        title="Photo C (No Date)",
        description="Has description",
        capture_date=None,
        original_image=ContentFile(img_io.getvalue(), name='test_c.jpg')
    )
    print(f"Created Photo C: {photo_c.title} (ID: {photo_c.id})")

    # 2. Test Gallery Endpoint
    factory = APIRequestFactory()
    view = GalleryView.as_view()
    
    request = factory.get('/api/photos/gallery/')
    force_authenticate(request, user=buyer)
    
    response = view(request)
    
    print("\n--- Gallery Response ---")
    print(f"Status Code: {response.status_code}")
    results = response.data
    if isinstance(results, dict) and 'results' in results:
        results = results['results']

    found_ids = [item['id'] for item in results]
    found_titles = [item['title'] for item in results]
    
    print(f"Returned Photo IDs: {found_ids}")
    print(f"Returned Titles: {found_titles}")

    # 3. Validation
    errors = []
    if photo_a.id not in found_ids:
        errors.append("❌ Photo A (Complete) was NOT returned!")
    else:
        print("✅ Photo A was returned correctly.")

    if photo_b.id in found_ids:
        errors.append("❌ Photo B (No Desc) was returned (Should be filtered)!")
    else:
        print("✅ Photo B was correctly filtered out.")

    if photo_c.id in found_ids:
        errors.append("❌ Photo C (No Date) was returned (Should be filtered)!")
    else:
        print("✅ Photo C was correctly filtered out.")

    if not errors:
        print("\n🏆 SUCCESS: Filtering logic passed all checks!")
    else:
        print("\n⚠️ FAILURES FOUND:")
        for e in errors:
            print(e)

if __name__ == "__main__":
    test_gallery_filtering()

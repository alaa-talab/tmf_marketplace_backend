import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib import admin
from photos.models import Photo
from users.models import User

print("Checking Admin Registry...")
if Photo in admin.site._registry:
    print("✅ Photo model is registered in Admin.")
else:
    print("❌ Photo model is NOT registered.")

if User in admin.site._registry:
    print("✅ User model is registered in Admin.")
else:
    print("❌ User model is NOT registered.")

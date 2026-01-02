from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploader', 'capture_date', 'created_at')
    list_filter = ('uploader', 'capture_date')
    search_fields = ('title', 'description', 'uploader__username')
    readonly_fields = ('watermarked_image', 'created_at')

admin.site.register(Photo, PhotoAdmin)

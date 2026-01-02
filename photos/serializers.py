from rest_framework import serializers
from .models import Photo

class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'description', 'capture_date', 'original_image']
        read_only_fields = ['id']

class PhotoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'description', 'capture_date', 'watermarked_image']

class PhotoDownloadSerializer(serializers.ModelSerializer):
    original_image_url = serializers.SerializerMethodField()
    watermarked_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'title', 'original_image_url', 'watermarked_image_url']

    def get_original_image_url(self, obj):
        if obj.original_image:
            # S3 URLs are already absolute, don't use build_absolute_uri
            url = obj.original_image.url
            # Only build absolute URI if it's a local path (starts with /)
            if url.startswith('/'):
                request = self.context.get('request')
                return request.build_absolute_uri(url) if request else url
            return url
        return None

    def get_watermarked_image_url(self, obj):
        if obj.watermarked_image:
            # S3 URLs are already absolute, don't use build_absolute_uri
            url = obj.watermarked_image.url
            # Only build absolute URI if it's a local path (starts with /)
            if url.startswith('/'):
                request = self.context.get('request')
                return request.build_absolute_uri(url) if request else url
            return url
        return None

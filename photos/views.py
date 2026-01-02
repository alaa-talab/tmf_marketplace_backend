from rest_framework import generics, permissions
from .models import Photo
from .serializers import PhotoUploadSerializer, PhotoGallerySerializer, PhotoDownloadSerializer
from .permissions import IsUploader, IsBuyer

class UploadPhotoView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoUploadSerializer
    permission_classes = [IsUploader]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class GalleryView(generics.ListAPIView):
    serializer_class = PhotoGallerySerializer
    permission_classes = [permissions.AllowAny]  # Public access

    def get_queryset(self):
        # Filter for non-empty Title, Description, and capture_date.
        # Capture date is not null by default, but we can check validation.
        # Exclude empty strings for title and description.
        return Photo.objects.exclude(title__exact='').exclude(description__exact='').exclude(capture_date__isnull=True).order_by('-created_at')

class PhotoDownloadView(generics.RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoDownloadSerializer
    permission_classes = [permissions.IsAuthenticated] # Access to download links for any auth user? Or specific?
    # User said "Return links to both", presumably for someone who bought it or the uploader. 
    # Let's keep it IsAuthenticated for now as requested range doesn't specify payment logic yet.

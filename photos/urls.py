from django.urls import path
from .views import UploadPhotoView, GalleryView, PhotoDownloadView

urlpatterns = [
    path('upload/', UploadPhotoView.as_view(), name='photo-upload'),
    path('gallery/', GalleryView.as_view(), name='photo-gallery'),
    path('download/<int:pk>/', PhotoDownloadView.as_view(), name='photo-download'),
]

from django.urls import path
from .views import FileUploadAPIView, FileDownloadAPIView

urlpatterns = [
    path('upload/', FileUploadAPIView.as_view(), name='file-upload'),
    path('download/<file_id>/', FileDownloadAPIView.as_view(), name='file-download'),
]

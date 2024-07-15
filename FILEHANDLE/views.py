from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import File
from .serializers import FileSerializer
from django.core.exceptions import ValidationError
from django.http import FileResponse
from django.conf import settings
import os

class FileUploadAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file = file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDownloadAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id, format=None):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            file = File.objects.get(pk=file_id)
        except File.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
            response['Content-Type'] = 'application/octet-stream'  
            return response
        else:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

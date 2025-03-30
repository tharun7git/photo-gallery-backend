# api/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from photoapp.models import Photo, Folder
from .serializers import PhotoSerializer, FolderSerializer, UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only access their own folders
        return Folder.objects.filter(user=self.request.user)

class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only access their own photos
        queryset = Photo.objects.filter(user=self.request.user)
        
        # Filter by folder if folder_id is provided
        folder_id = self.request.query_params.get('folder', None)
        if folder_id:
            queryset = queryset.filter(folder_id=folder_id)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def move_to_folder(self, request, pk=None):
        photo = self.get_object()
        folder_id = request.data.get('folder_id')
        
        try:
            # Check if folder exists and belongs to user
            folder = Folder.objects.get(id=folder_id, user=request.user)
            photo.folder = folder
            photo.save()
            return Response({'status': 'photo moved'}, status=status.HTTP_200_OK)
        except Folder.DoesNotExist:
            return Response({'error': 'Folder not found'}, status=status.HTTP_404_NOT_FOUND)
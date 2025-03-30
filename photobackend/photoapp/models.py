# photoapp/models.py
from django.db import models
from django.conf import settings

class Folder(models.Model):
    """Folder model to organize photos"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    class Meta:
        unique_together = ['name', 'user']  # Prevent duplicate folder names for a user

class Photo(models.Model):
    """Photo model to store images"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
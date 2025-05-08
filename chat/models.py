from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Room(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
def get_timestamp_with_offset():
    return timezone.now() + timedelta(hours=3)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=get_timestamp_with_offset)
    
    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
    
    class Meta:
        ordering = ['timestamp']

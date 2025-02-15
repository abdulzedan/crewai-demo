# backend/app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Our custom user model with an extra 'bio' field.
    """
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class UserText(models.Model):
    user = models.ForeignKey("app.CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"UserText #{self.id} - {self.content[:30]}"

class StoredResume(models.Model):
    user = models.ForeignKey("app.CustomUser", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"StoredResume #{self.id} - {self.content[:30]}"

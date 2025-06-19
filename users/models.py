from django.db import models
from django.contrib.auth.models import User
import json
import datetime
LANGUAGE_CHOICES = (
    ('en','English'),
    ('vi', 'Vietnamese'),
) 
DIFFICULTY_CHOICES = (
    ('BEGINNER','Beginner'),
    ('INTERMEDIATE','Intermediate'),
    ('ADVANCED','Advanced')
)
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = 'profile'
    )
    full_name = models.CharField(
        max_length = 100,
        blank = True,
        null = True
    )
    created_at = models.DateTimeField(
        auto_now_add = True
    )
    updated_at = models.DateTimeField(
        auto_now = True
    )
    language_preference = models.CharField(
        max_length = 10,
        choices = LANGUAGE_CHOICES,
        default = 'en'
    )
    preferred_programming_languages = models.JSONField(
        default = list,
        blank = True
    )
    difficulty_preference = models.CharField(
        max_length = 20,
        choices = DIFFICULTY_CHOICES,
        default = 'BEGINNER'
    )
    email_notification = models.BooleanField(
        default = True
    )
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields =['language_preference']),
            models.Index(fields = ['-created_at']),
        ]
    def _str_(self):
        return f"Profile for {self.user.username}"
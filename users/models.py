from django.db import models
from django.contrib.auth.models import User
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
class Project(models.Model):
    checklist_items = models.JSONField()
class ProjectProgress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    completed_items = models.JSONField()
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
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    total_projects = models.IntegerField(default=0)
    completed_projects = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    current_level = models.CharField(max_length=20, default='BEGINNER')
    learning_goals = models.CharField(max_length=20, blank=True)
    target_daily_hours = models.IntegerField(default=1)
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
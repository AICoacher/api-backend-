from rest_framework import serializers
from .models import UserProfile  
from .models import UserProfile, ProjectProgress
class UserProfileSerializer(serializers.ModelSerializer):
    completion_rate = serializers.SerializerMethodField() 
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    def get_completion_rate(self,obj):
        total_completion = 0
        project_count = 0
        user = obj.user
        user_projects = ProjectProgress.objects.filter(user = user)
        for project_progress in user_projects:
            checklist_items = project_progress.project.checklist_items
            completed_items = project_progress.completed_items
            project_completion = len(completed_items) / len(checklist_items) * 100
            total_completion += project_completion
            project_count += 1
        overall_rate = total_completion / project_count if project_count > 0 else 0
        return overall_rate
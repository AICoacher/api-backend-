from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Project, ProjectProgress
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView  
from rest_framework.permissions import AllowAny
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return UserProfile.objects.filter(user = self.request.user) 
    @action(detail = False, methods=['get'])
    def me(self, request):
        try:
            profile = self.get_queryset().first()
            if not profile:
                return Response(
                    {'error': 'Profile not found'},
                    status = status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Internal server error'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @action(detail = False, methods=['get'])
    def dashboard(self, request):
        try:
            user = request.user
            profile = UserProfile.objects.get(user = user)
            if not profile:
                return Response(
                    {'error':'Profile not found'},
                    status = status.HTTP_404_NOT_FOUND
                )
            user_projects = ProjectProgress.objects.filter(user = user)
            total_completion = 0
            project_count = 0
            for project_progress in user_projects:
                checklist_items = project_progress.project.checklist_items
                completed_items = project_progress.completed_items
                project_completion = len(completed_items) / len(checklist_items) * 100
                total_completion += project_completion
                project_count += 1
            overall_rate = total_completion / project_count if project_count > 0 else 0
            dashboard_data = {
                'user_stats':{
                    'total_projects' : profile.total_projects,
                    'completed_projects': profile.completed_projects,
                    'current_streak': profile.current_streak,
                    'total_points': profile.total_points,
                    'completion_rate':overall_rate,
                    'experience_level': profile.total_points/100,
                    'active_projects_count': project_count-total_completion
                }
            }
            return Response(dashboard_data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Internal server error'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email','')
            if not username or not password:
                return Response(
                    {'error': 'Username and password are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(username = username).exists():
                return Response({'error': 'username already exists'},status = status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, password = password, email = email)
            UserProfile.objects.create(user=user)
            return Response({'message': 'User registered successfully'}, status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': 'Invalid request data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        




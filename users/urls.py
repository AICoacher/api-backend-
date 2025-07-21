from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet
from django.urls import path
from .views import UserProfileViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
]

from django.urls import path
from .views import (
    CategoryListView,
    LoginView,
    CustomRegistrationView,
    VideoDetailView,
    VideoView,
    ActivationAPIView,
    RequestPasswordResetView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', CustomRegistrationView.as_view(), name='django_registration_register'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('videos/<int:id>/', VideoDetailView.as_view(), name='video-detail'), 
    path('video_selection/', VideoView.as_view(), name='video_selection'),
    path('activate/<str:uidb64>/<str:token>/', ActivationAPIView.as_view(), name='activation-api'),
    path('password-reset/', RequestPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
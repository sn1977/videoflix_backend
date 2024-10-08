# """videoflix_backend URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include
# from django.conf.urls.static import static
# from django.conf import settings
# import debug_toolbar

# from content.views import ActivationAPIView, LoginView, CustomRegistrationView, PasswordResetConfirmView, RequestPasswordResetView, VideoView


# # //NOTE - this is for testing Sentry
# def trigger_error(request):
#     division_by_zero = 1 / 0


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('content.api_urls')),
#     path('login/', LoginView.as_view(), name='login'),
#     # path('register/', RegisterView.as_view()),
#     path('register/', CustomRegistrationView.as_view(), name='django_registration_register'),
#     path('video_selection/', VideoView.as_view(), name='register'),
#     path('activate/<str:uidb64>/<str:token>/', ActivationAPIView.as_view(), name='activation-api'),
#     path('accounts/', include('django_registration.backends.activation.urls')),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('password-reset/', RequestPasswordResetView.as_view(), name='password_reset'),
#     path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('__debug__/', include(debug_toolbar.urls)),
#     path('django-rq/', include('django_rq.urls')),
#     path('sentry-debug/', trigger_error) # //NOTE - this is for testing Sentry
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

from content.views import ActivationAPIView, LoginView, CustomRegistrationView, PasswordResetConfirmView, RequestPasswordResetView, VideoView

# //NOTE - this is for testing Sentry
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('content.api_urls')),  # Füge dies hinzu
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('django-rq/', include('django_rq.urls')),
    path('sentry-debug/', trigger_error) # //NOTE - this is for testing Sentry
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
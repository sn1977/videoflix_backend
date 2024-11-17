from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

from content.views import ActivationAPIView, LoginView, CustomRegistrationView, PasswordResetConfirmView, RequestPasswordResetView, VideoView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
] + staticfiles_urlpatterns()
#  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

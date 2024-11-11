from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from content.models import Category, Video
from content.serializers import (
    CategorySerializer,
    EmailOrUsernameAuthTokenSerializer,
    RegisterSerializer,
    VideoSerializer,
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status

from django_registration.backends.activation.views import RegistrationView


from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from django_registration.backends.activation import ActivationBackend
from django.contrib.auth.tokens import default_token_generator


from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

import logging

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

# Create your views here.


# TODO - dies muss für das caching bei einer View gemacht werden!

# 09 - Redis Caching
# Guter Artikel: https://realpython.com/caching-in-django-with-redis/
# In der views.py
# from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Über die FunktionÜber die Funktion
# @cache_page(CACHE_TTL)


class LoginView(ObtainAuthToken):
    """
    View for handling user login and returning an authentication token.

    This view extends ObtainAuthToken and uses the EmailOrUsernameAuthTokenSerializer
    to validate the user's credentials. Upon successful authentication, it returns
    a response containing the authentication token, user ID, email, and username.

    Methods:
      post(request, *args, **kwargs):
        Handles POST requests for user login. Validates the provided credentials
        and returns an authentication token along with user details.

    Decorators:
      @method_decorator(cache_page(CACHE_TTL)):
        Caches the response for the duration specified by CACHE_TTL.
    """
    serializer_class = EmailOrUsernameAuthTokenSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "username": user.username,
            }
        )
        
        
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('videos').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    
class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {'request': self.request}


class VideoView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class CustomRegistrationView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(cache_page(CACHE_TTL))
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User created successfully. Please check your email to activate your account."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_activation_email(user):
    # Generiere Token und UID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Erstelle die Aktivierungs-URL
    activation_url = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"

    # E-Mail Betreff
    subject = "Activate your account"

    # Reine Text-Nachricht (Fallback)
    plain_message = f"""
    Dear {user.first_name} {user.last_name},

    Thank you for registering with Videoflix. To complete your registration and verify your email address, please click the link below:

    {activation_url}

    If you did not create an account with us, please disregard this email.

    Best regards,
    Your Videoflix Team
    """

    # HTML-Nachricht
    html_message = f"""
    <div style="text-align: center; margin-bottom: 20px;">
              <img src="http://localhost:4200/assets/img/logo_transparent.png" alt="Videoflix Logo" style="max-width: 200px; height: auto;">
    </div>
    
    <p>Dear {user.first_name} {user.last_name},</p>
    
    <p>Thank you for registering with <span style="color:#0d6efd;">Videoflix</span>. To complete your registration and verify your email address, please click the link below:</p>
    
    <p>
        <a href="{activation_url}" style="
            background-color: #0d6efd;
            color: white;
            text-decoration: none;
            padding: 0.5em 1.5em;
            border-radius: 3em;
        ">
            Activate Account
        </a>
    </p>
    
    <p>If you did not create an account with us, please disregard this email.</p>
    
    <p>Best regards,</p>
    <p>Your Videoflix Team</p>
    """

    # Absender und Empfänger
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Sende die E-Mail mit HTML-Inhalt
    send_mail(
        subject=subject,
        message=plain_message,  # Reine Text-Nachricht
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,  # HTML-Nachricht
    )


class ActivationAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, format=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            User = get_user_model()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"message": "Account successfully activated."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Activation link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Passe die Domain an
            reset_url = f"http://localhost:4200/reset-password/{uid}/{token}/"
            subject = "Reset your password"
            # Reine Text-Nachricht (Fallback)
            plain_message = f"To reset your password, follow this link: {reset_url}"

            # HTML-Nachricht
            html_message = f"""
            <p>Dear {user.first_name} {user.last_name},</p>
            
            <p>We recently received a request to reset your password. If you made this request, please click on the following link to reset your password:</p>
            
            <p>
                <a href="{reset_url}" style="
                    background-color: #0d6efd;
                    color: white;
                    text-decoration: none;
                    padding: 0.5em 1.5em;
                    border-radius: 3em;
                    display: inline-block;
                ">
                    Reset password
                </a>
            </p>
            
            <p>Please note that for security reasons, this link is only valid for 24 hours.</p>
            
            <p>If you did not request a password reset, please ignore this email.</p>
            
            <p>Best regards,</p>
            <p>Your Videoflix Team</p>
            
            <div style="text-align: center; margin-bottom: 20px;">
              <img src="http://localhost:4200/assets/img/logo_transparent.png" alt="Videoflix Logo" style="max-width: 200px; height: auto;">
            </div>
            """

            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            # Sende die E-Mail mit HTML-Inhalt
            send_mail(
                subject=subject,
                message=plain_message,  # Reine Text-Nachricht
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,  # HTML-Nachricht
            )

            logger.info(f"Password reset email sent to {user.email}")

            return Response(
                {"message": "Password reset link has been sent to your email."},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            # Aus Sicherheitsgründen geben wir dieselbe Antwort zurück
            return Response(
                {"message": "Password reset link has been sent to your email."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error sending password reset email to {email}: {e}")
            return Response(
                {"error": "An error occurred while sending the password reset email."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get("password")

        if not password:
            return Response(
                {"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            User = get_user_model()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST
            )

        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

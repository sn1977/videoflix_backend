from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from content.models import Video
from content.serializers import RegisterSerializer, VideoSerializer
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


# Create your views here.


# TODO - dies muss für das caching bei einer View gemacht werden!

# 09 - Redis Caching
# Guter Artikel: https://realpython.com/caching-in-django-with-redis/
# In der views.py
# from django.core.cache.backends.base import DEFAULTTIMEOUT
# from django.views.decorators.cache importcachepage from django.conf import settings

# CACHETTL = getattr(settings, 'CACHETTL', DEFAULT_TIMEOUT)

# Über die FunktionÜber die Funktion
# @cachepage(CACHETTL)


class LoginView(ObtainAuthToken):
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


class VideoView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name='dispatch')
class CustomRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_activation_email(user, request)
            return Response({
                "message": "User created successfully. Please check your email to activate your account."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_activation_email(self, user, request):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = f'http://localhost:4200/activate/{uid}/{token}/'  # Passen Sie die Domain an
        subject = 'Activate your account'
        # message = f'Please activate your account by clicking the following link: {activation_url}'
        message = f'Dear {user.first_name} {user.last_name},\n\nPlease activate your account by clicking the following link:\n{activation_url}\n\nThank you! Your Videoflix-Team'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

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
            return Response({'message': 'Account successfully activated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)
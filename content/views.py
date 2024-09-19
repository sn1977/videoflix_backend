from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from content.models import Video
from content.serializers import RegisterSerializer, VideoSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status

from django_registration.backends.activation.views import RegistrationView


from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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


# class RegisterView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = []

#     def post(self, request, format=None):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response(
#                 {
#                     "token": token.key,
#                     "user_id": user.pk,
#                     "username": user.username,
#                     "email": user.email,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({
#                 "user": RegisterSerializer(user).data,
#                 "message": "User created successfully."
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
@method_decorator(csrf_exempt, name='dispatch')  # CSRF-Schutz für diese View deaktivieren
class CustomRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Benutzer inaktiv setzen, bis E-Mail bestätigt wurde
            user.save()
            # Aktivierungs-E-Mail senden
            self.send_activation_email(user, request)
            return Response({
                "message": "User created successfully. Please check your email to activate your account."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_activation_email(self, user, request):
        from django_registration.backends.activation.views import RegistrationView
        registration_view = RegistrationView()
        activation_key = registration_view.get_activation_key(user)
        activation_url = request.build_absolute_uri(
            reverse('django_registration_activate', args=[activation_key])
        )
        subject = 'Activate your account'
        message = f'Please activate your account by clicking the following link: {activation_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
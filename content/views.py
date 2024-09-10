from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from content.models import Video
from content.serializers import VideoSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.


#TODO - dies muss für das caching bei einer View gemacht werden!

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
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })
        
class VideoView(generics.ListCreateAPIView):
  queryset = Video.objects.all()
  serializer_class = VideoSerializer

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  # def perform_create(self, serializer):
  #   serializer.save(owner=self.request.user)

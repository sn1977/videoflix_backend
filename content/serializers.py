from rest_framework import serializers
from content.models import Category, Video
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, CharField

from users.models import CustomUser 

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


# class VideoSerializer(serializers.ModelSerializer):
#     hls_url = serializers.ReadOnlyField()

#     class Meta:
#         model = Video
#         fields = '__all__'
        
class VideoSerializer(serializers.ModelSerializer):
    hls_url = serializers.SerializerMethodField()
    video_file = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_hls_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.hls_url)
        return obj.hls_url

    def get_video_file(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.video_file.url)
        return obj.video_file.url
      
    def get_thumbnail(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return request.build_absolute_uri(obj.thumbnail.url)
        return ''  
      
class CategorySerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)  # Videos in der Kategorie

    class Meta:
        model = Category
        fields = ['id', 'name', 'videos']
    
class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=False  # Benutzer ist inaktiv bis zur Aktivierung
        )
        user.set_password(validated_data['password'])
        user.save()
        return user   
      
      
      
class EmailOrUsernameAuthTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(label=_("Email or Username"), write_only=True)
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Versuche, den Benutzer anhand des Benutzernamens zu authentifizieren
            user = authenticate(request=self.context.get('request'), username=email_or_username, password=password)
            if not user:
                # Versuche, den Benutzer anhand der E-Mail zu authentifizieren
                UserModel = get_user_model()
                try:
                    user_obj = UserModel.objects.get(email=email_or_username)
                    # user_qs = UserModel.objects.filter(email=email_or_username)
                    user = authenticate(request=self.context.get('request'), username=user_obj.username, password=password)
                except UserModel.DoesNotExist:
                    pass

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email_or_username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs       
      
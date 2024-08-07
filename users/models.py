from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    custom = models.CharField(max_length=1000, default="", blank=True)
    phone = models.CharField(max_length=20, default="")
    street = models.CharField(max_length=150, default="")
    postal_code = models.CharField(max_length=15, default="")
    city = models.CharField(max_length=20, default="")

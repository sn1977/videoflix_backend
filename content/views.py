from django.shortcuts import render

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
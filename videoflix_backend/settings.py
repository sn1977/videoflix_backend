import os
from pathlib import Path
from xml.etree.ElementInclude import default_loader
import sentry_sdk
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(v5fm-b0v5(+_u5og6hfs^q*7v=9t_hjevxhuu^m=jc5ft(ane"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "35.242.235.177", "gc-videoflixbackend.sascha-nemeth.com"]

CORS_ALLOWED_ORIGINS = ["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:50453", "https://videoflix.sascha-nemeth.com"]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",
]

CACHE_TTL = 60 * 15  # 15 minutes

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    'django_registration',
    'django.contrib.sites',  # Notwendig für django-registration
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "content.apps.ContentConfig",
    "debug_toolbar",
    "django_rq",
    "import_export",
    # "users",
    'users.apps.UsersConfig',
    "rest_framework",
    "rest_framework.authtoken",
]

SITE_ID = 1  # Stelle sicher, dass dies gesetzt ist

AUTH_USER_MODEL = "users.CustomUser"

IMPORT_EXPORT_USE_TRANSACTIONS = True

# STATIC_ROOT = os.path.join(BASE_DIR, "static/staticfiles")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = [
    # Füge deine IP-Adresse hinzu. Zum Beispiel:
    "127.0.0.1",
]

RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        # 'USERNAME': 'some-user',
        # 'PASSWORD': 'some-password',
        "DEFAULT_TIMEOUT": 360,
        # 'REDIS_CLIENT_KWARGS': {    # Eventual additional Redis connection arguments
        #     'ssl_cert_reqs': None,
        # },
    },
    # 'high': {
    #     'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
    #     'DEFAULT_TIMEOUT': 500,
    # },
    # 'low': {
    #     'HOST': 'localhost',
    #     'PORT': 6379,
    #     'DB': 0,
    # }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "videoflix",
    }
}
ROOT_URLCONF = "videoflix_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

WSGI_APPLICATION = "videoflix_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = "static/"
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


sentry_sdk.init(
    dsn="https://a4fef9e49d1c7225b0095c56cc06e011@o4507877077024768.ingest.de.sentry.io/4507877122834512",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        # 'rest_framework.authentication.TokenAuthentication',
    ]
}

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window

# settings.py

load_dotenv()

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Zum Testen

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL') == 'True'
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Frontend-URL für Aktivierungslinks
FRONTEND_URL = os.environ.get('FRONTEND_URL')

# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

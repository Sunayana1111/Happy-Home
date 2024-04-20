from pathlib import Path
from .env import *

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1ko4g-omc6ey-bess23i^hk+c437=^&b!nbybo6v@3tcpz*qv!'

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'account',
    'commons',
    "core",
    "corsheaders",
    "chat",
    "channels",
    "dashboard"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'happy_home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'happy_home.wsgi.application'
ASGI_APPLICATION = 'happy_home.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # "rest_framework.renderers.BrowsableAPIRenderer"# Use JSONRenderer as the default
        # Add other renderer classes if needed
    ],
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10
}


LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'
LOGIN_REDIRECT_URL = '/api/root/'
LOGOUT_REDIRECT_URL = '/api/root/'
CORS_ORIGIN_ALLOW_ALL = True

KHALTI_PUBLIC_KEY = khalti_public_key
KHALTI_SECRET_KEY = khalti_secret_key

CSRF_TRUSTED_ORIGINS = [
    'https://e7ae-2400-1a00-b030-162d-cb8-de70-bc62-2342.ngrok-free.app',  # Add your trusted host here
    'https://subdomain.example.com',  # Add additional trusted hosts if needed
]


# DEFAULT_FROM_EMAIL = 'Happy Home <noreply@munanyc.com>'
TO_EMAIL = 'sunayanashrestha3@gmail.com'

# EMAIL_HOST = 'email-smtp.ap-southeast-1.amazonaws.com'
# EMAIL_HOST_USER = 'AKIAT5H336S4II2D5KAF'
# EMAIL_HOST_PASSWORD = 'BNircvi19pDA+G4uGijCICYJdSRotX9ySOlyUVWdsXmu'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True


# AWS Email
DEFAULT_FROM_EMAIL = 'Happy Home <noreply@levelup.com.np>'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_HOST_USER = 'AKIA3J3FUXCJIBP6OQUR'
EMAIL_HOST_PASSWORD = 'BIG/JGOJ9+nRWCLqN8/x2e8V/KNBYAgNKaimCxhToL1C'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'happyhomedb',
#         'USER': 'mysql',
#         'PASSWORD': '',
#         'HOST': 'localhost',  # Or your MySQL server IP address
#         'PORT': '3306',  # MySQL default port
#     }
# }

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'ngrok-skip-browser-warning'
]

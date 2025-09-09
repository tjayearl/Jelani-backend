import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-insecure-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Load hosts from environment variable, defaulting to local development hosts.
ALLOWED_HOSTS = []
if 'ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS.extend(os.environ.get('ALLOWED_HOSTS').split(','))
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', 'testserver'])

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_rest_passwordreset',
    'django_extensions',
    'accounts',
    'user_accounts',   # new app
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)

ROOT_URLCONF = 'jelani_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'jelani_backend.wsgi.application'

# Database configuration.
# The default is set to SQLite for simple local development.
# For production, you can override this by setting the DATABASE_URL environment variable.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Custom User Model
# AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend', # Custom backend for email/username login
    'django.contrib.auth.backends.ModelBackend',     # Default backend for Django admin
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT Settings
SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Use a long-lived access token in development for easier testing
if DEBUG:
    SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(days=1)
else:
    # Keep it short in production for security
    SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=15)


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# CORS Settings
# A list of origins that are authorized to make cross-site HTTP requests.
CORS_ALLOWED_ORIGINS = [
    "https://jelani-afrika.vercel.app",  # Production frontend
    "http://localhost:5500",             # Local testing
]
CORS_ALLOW_CREDENTIALS = True # Allow cookies to be sent with requests

# Static files (CSS, JavaScript, Images) for Django Admin
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User-uploaded content like claim documents)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

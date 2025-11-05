"""
Django settings for devapp project.
"""

from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# Security
# =====================
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key')  # override in production
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost",
    
).split(",")

# =====================
# Applications
# =====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devapp.urls'
WSGI_APPLICATION = 'devapp.wsgi.application'

# =====================
# Templates
# =====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =====================
# Database
# =====================
if os.getenv("DATABASE_HOST"):  # Koyeb Postgres
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("DATABASE_NAME", "koyebdb"),
            'USER': os.getenv("DATABASE_USER", "koyeb-adm"),
            'PASSWORD': os.getenv("DATABASE_PASSWORD", ""),
            'HOST': os.getenv("DATABASE_HOST", ""),
            'PORT': os.getenv("DATABASE_PORT", "5432"),
            'OPTIONS': {'sslmode': 'require'},
        }
    }
else:  # Local SQLite fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =====================
# Static & Media
# =====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']  # local dev assets
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =====================
# Email
# =====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# =====================
# Password Validators
# =====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =====================
# Localization
# =====================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = 'd/m/Y'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'd/m/Y H:i:s'

DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y %H:%M:%S',
]

# =====================
# Default primary key field type
# =====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

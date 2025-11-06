from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.files.storage import FileSystemStorage
# Import GoogleDriveStorage for use inside the conditional function
try:
    from gdstorage.storage import GoogleDriveStorage
except ImportError:
    # Allows settings to load even if gdstorage is not installed (e.g., lightweight dev environment)
    GoogleDriveStorage = None

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
    'gdstorage',
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
                # The incorrect line 'django.template.context_processors.messages' 
                # has been removed to fix the ImportError.
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
# Use Path object for consistency
MEDIA_ROOT = BASE_DIR / 'media' 


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
# USE_L10N is deprecated in Django 4.0+. Using USE_TZ=True usually supersedes L10N for dates/times.
# USE_L10N = True 
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


# =====================
# CONDITIONAL FILE STORAGE
# =====================

# Global settings used by gdstorage, defined here but only populated inside the function
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS = None
GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = 'vasudev_products' 


def get_file_storage_instance():
    """
    Dynamically initializes and returns the correct storage backend.
    
    This function is used in models.py (storage=get_file_storage_instance) 
    to defer storage initialization until runtime, preventing a crash when 
    running manage.py commands locally without the key.
    """
    
    # Check for PRODUCTION mode (not DEBUG) and if the required key is available
    if not DEBUG and os.environ.get('GOOGLE_DRIVE_KEY_JSON'):
        # PRODUCTION (Koyeb) - Use Google Drive Storage
        if GoogleDriveStorage:
             # The storage package uses GOOGLE_DRIVE_STORAGE_... settings automatically
            global GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS
            GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS = os.environ.get('GOOGLE_DRIVE_KEY_JSON')
            
            print("Using Google Drive Storage...")
            return GoogleDriveStorage()
        else:
            # Should not happen if gdstorage is in INSTALLED_APPS
            print("WARNING: gdstorage not imported. Falling back to local FS.")
            return FileSystemStorage(location=MEDIA_ROOT)
    else:
        # DEVELOPMENT (Local) - Use Local File System Storage
        print("Using Local File System Storage...")
        return FileSystemStorage(location=MEDIA_ROOT)

# This variable is referenced by models.py using 'settings.FILE_STORAGE_FUNCTION'
FILE_STORAGE_FUNCTION = get_file_storage_instance
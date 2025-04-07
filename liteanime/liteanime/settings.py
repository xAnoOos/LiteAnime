from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-a8ev8na1cs*7r!5u0g9supnta0@69iuj=)+k-4$h(l2_k^d7n1'
DEBUG = True

ALLOWED_HOSTS = ['16.171.40.48', 'localhost', '127.0.0.1', 'liteanime.com']

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "liteanime" / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Application definition
INSTALLED_APPS = [
    'core',
    'news',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'liteanime.urls'

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
                'core.context_processors.unread_notifications_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'liteanime.wsgi.application'

CSRF_TRUSTED_ORIGINS = [
    'https://liteanime.com',
    'https://www.liteanime.com'
]


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'root',
        'PASSWORD': 'LITEanimezx99@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'core.validators.CustomPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Secure cookies & HTTPS redirect (important in production)
SECURE_SSL_REDIRECT = False  # i will change to true when uploaded (to open in https insted of http)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

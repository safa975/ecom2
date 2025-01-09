import os
from pathlib import Path
from django.conf import settings


BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_DIR = BASE_DIR / 'templates'

SECRET_KEY = 'django-insecure-365*9ymwu3u$z&a69pms&!tvlj5cl^b#*e048_8l9=5m=p3yv$'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1','localhost']

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'phonenumber_field',
    'adminpanel',
    'home',
    'payment',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.getcwd(), 'templates')],
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


WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Ensure this is the correct engine for PostgreSQL
        'NAME': 'cupcraze',
        'USER': 'cupcraze_user',
        'PASSWORD': 'cupcraze123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Static and Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py

# Email Backend Configuration (For development, use console backend to log emails in the console)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'fathimathusafa7@gmail.com'  
EMAIL_HOST_PASSWORD = 'rzpj wxqr ycib xfqk'
DEFAULT_FROM_EMAIL = 'fathimathusafa7@gmail.com'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'


# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'

import environ

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

RAZORPAY_API_KEY_ID = env('RAZORPAY_API_KEY_ID', default=None)
RAZORPAY_API_SECRET = env('RAZORPAY_API_SECRET', default=None)

print("RAZORPAY_API_KEY_ID:", RAZORPAY_API_KEY_ID)
print("RAZORPAY_API_SECRET:", RAZORPAY_API_SECRET)

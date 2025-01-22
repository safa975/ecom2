import os
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Templates Directory
TEMP_DIR = BASE_DIR / 'templates'

# Security
SECRET_KEY = env('SECRET_KEY', default='your-default-secret-key')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'fathimathusafa.pythonanywhere.com',  
]

# Installed Apps
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME', default='cupcraze'),
        'USER': env('DATABASE_USER', default='cupcraze_user'),
        'PASSWORD': env('DATABASE_PASSWORD', default='cupcraze1234'),
        'HOST': env('DATABASE_HOST', default='fathimathusafa.pythonanywhere.com'),
        'PORT': env('DATABASE_PORT', default='5432'),
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

# Email Backend Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='your-email@example.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='your-email-password')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Session Engine
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Razorpay API Configuration
RAZORPAY_API_KEY_ID = env('RAZORPAY_API_KEY_ID', default=None)
RAZORPAY_API_SECRET = env('RAZORPAY_API_SECRET', default=None)

# Debugging Razorpay API keys (optional, remove in production)
print("RAZORPAY_API_KEY_ID:", RAZORPAY_API_KEY_ID)
print("RAZORPAY_API_SECRET:", RAZORPAY_API_SECRET)

import os
import sys

# Add your project path
sys.path.append('/home/Fathimathusafa/ecommerce')

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

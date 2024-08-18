"""
Django settings for arpansahu_dot_me project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# ============================ENV VARIABLES=====================================
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(' ')

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
BUCKET_TYPE = config('BUCKET_TYPE')

DATABASE_URL = config('DATABASE_URL')
REDIS_CLOUD_URL = config('REDIS_CLOUD_URL')

MAIL_JET_API_KEY = config('MAIL_JET_API_KEY')
MAIL_JET_API_SECRET = config('MAIL_JET_API_SECRET')
MAIL_JET_EMAIL_ADDRESS = config('MAIL_JET_EMAIL_ADDRESS')
MY_EMAIL_ADDRESS = config('MY_EMAIL_ADDRESS')

SENTRY_ENVIRONMENT = config('SENTRY_ENVIRONMENT')  # production Or "staging", "development", etc.
SENTRY_ENVIRONMENT

PROJECT_NAME = 'arpansahu_dot_me'
# ===============================================================================

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom apps
    'check_service_health',
    'custom_tag_app',
    'account',
    'emails_otp',
    'resume'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'arpansahu_dot_me.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'arpansahu_dot_me.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }

# Parse database configuration from $DATABASE_URL
import dj_database_url

# DATABASES['default'] =  dj_database_url.config()
# updated
DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

if not DEBUG:
    BUCKET_TYPE = BUCKET_TYPE

    if BUCKET_TYPE == 'AWS':
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400'
        }
        AWS_LOCATION = 'static'
        AWS_QUERYSTRING_AUTH = False
        AWS_HEADERS = {
            'Access-Control-Allow-Origin': '*',
        }
        # s3 static settings
        AWS_STATIC_LOCATION = f'portfolio/{PROJECT_NAME}/static'
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
        STATICFILES_STORAGE = f'{PROJECT_NAME}.storage_backends.StaticStorage'
        # s3 public media settings
        AWS_PUBLIC_MEDIA_LOCATION = f'portfolio/{PROJECT_NAME}/media'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_PUBLIC_MEDIA_LOCATION}/'
        DEFAULT_FILE_STORAGE = f'{PROJECT_NAME}.storage_backends.PublicMediaStorage'
        # s3 private media settings
        PRIVATE_MEDIA_LOCATION = f'portfolio/{PROJECT_NAME}/private'
        PRIVATE_FILE_STORAGE = f'{PROJECT_NAME}.storage_backends.PrivateMediaStorage'

    elif BUCKET_TYPE == 'BLACKBLAZE':
        AWS_S3_REGION_NAME = 'us-east-005'

        AWS_S3_ENDPOINT = f's3.{AWS_S3_REGION_NAME}.backblazeb2.com'
        AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_ENDPOINT}'
        
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
        }

        AWS_LOCATION = 'static'
        AWS_QUERYSTRING_AUTH = False
        AWS_HEADERS = {
            'Access-Control-Allow-Origin': '*',
        }
        # s3 static settings
        AWS_STATIC_LOCATION = f'portfolio/{PROJECT_NAME}/static'
        STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_STATIC_LOCATION}/'
        STATICFILES_STORAGE = f'{PROJECT_NAME}.storage_backends.StaticStorage'
        # s3 public media settings
        AWS_PUBLIC_MEDIA_LOCATION = f'portfolio/{PROJECT_NAME}/media'
        MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_PUBLIC_MEDIA_LOCATION}/'
        DEFAULT_FILE_STORAGE = f'{PROJECT_NAME}.storage_backends.PublicMediaStorage'
        # s3 private media settings
        PRIVATE_MEDIA_LOCATION = f'portfolio/{PROJECT_NAME}/private'
        PRIVATE_FILE_STORAGE = f'{PROJECT_NAME}.storage_backends.PrivateMediaStorage'

    elif BUCKET_TYPE == 'MINIO':
        AWS_S3_REGION_NAME = 'us-east-1'  # MinIO doesn't require this, but boto3 does
        AWS_S3_ENDPOINT_URL = 'https://minio.arpansahu.me'
        AWS_DEFAULT_ACL = 'public-read'
        AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
        }
        AWS_LOCATION = 'static'
        AWS_QUERYSTRING_AUTH = False
        AWS_HEADERS = {
            'Access-Control-Allow-Origin': '*',
        }

        # s3 static settings
        AWS_STATIC_LOCATION = f'portfolio/{PROJECT_NAME}/static'
        STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}/{AWS_STATIC_LOCATION}/'
        STATICFILES_STORAGE = f'{PROJECT_NAME}.storage_backends.StaticStorage'

        # s3 public media settings
        AWS_PUBLIC_MEDIA_LOCATION = f'portfolio/{PROJECT_NAME}/media'
        MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}/{AWS_PUBLIC_MEDIA_LOCATION}/'
        DEFAULT_FILE_STORAGE = f'{PROJECT_NAME}.storage_backends.PublicMediaStorage'

        # s3 private media settings
        PRIVATE_MEDIA_LOCATION = 'portfolio/borcelle_crm/private'
        PRIVATE_FILE_STORAGE = 'borcelle_crm.storage_backends.PrivateMediaStorage'
else:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "account.Account"

# Login_required Decorator
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

LOGIN_REDIRECT_URL = "/"

OTP_EXPIRY_TIME = 60

# HTTP_X_FORWARDED_PROTO
SECURE_HSTS_SECONDS = 30  # Unit is seconds; *USE A SMALL VALUE FOR TESTING!*
SECURE_HSTS_SECONDS = 2_592_000  # 30 days
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# REFERRER POLICY
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

#Caching
if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_CLOUD_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': PROJECT_NAME
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Get the current git commit hash
def get_git_commit_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
    except Exception:
        return None

sentry_sdk.init(
    dsn="https://331f4612eb24264aada28947f75526c3@o4507787065163776.ingest.us.sentry.io/4507797138571264",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,  # Adjust this according to your needs
    send_default_pii=True,  # To capture personal identifiable information (optional)
    release=get_git_commit_hash(),  # Set the release to the current git commit hash
    environment=SENTRY_ENVIRONMENT,  # Or "staging", "development", etc.
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'ERROR',  # Change this to WARNING or INFO if needed
            'class': 'sentry_sdk.integrations.logging.EventHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',  # Only log errors to Sentry
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',  # Only log errors to Sentry
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',  # You can set this to INFO or DEBUG as needed
            'propagate': False,
        },
        # You can add more loggers here if needed
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
}

CSRF_TRUSTED_ORIGINS = ['https://arpansahu.me', ]
"""
Test settings for pytest.
Overrides production settings to use SQLite for testing.
"""
import os
from arpansahu_dot_me.settings import *

# Use file-based SQLite when TEST_DB_FILE is set (needed for UI tests where
# migrate and runserver run as separate processes sharing a database).
# Default to in-memory for fast unit tests.
_test_db = os.environ.get('TEST_DB_FILE', ':memory:')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _test_db,
    }
}

# Disable password hashers for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable debug for tests
DEBUG = False

# Use simple in-memory cache for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Disable email sending in tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Use local file storage for media in tests (override STORAGES if set)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Static files settings for tests
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Allow test hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'testserver']

# Disable security settings for tests
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


import os
from os import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(environ.get('DEBUG'))

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SITE_NAME = 'AHS'

INSTALLED_APPS = [
    # ASGI Server
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admindocs',

    # django channels
    'channels',
    'channels_redis',
    'rest_framework',
    'rest_framework_simplejwt',
    'adrf',
    'corsheaders',

    # webpack loader
    'whitenoise',
    'webpack_loader',

    # Toolbar Plugins/Modules
    'debug_toolbar',

    # Plugins/Modules
    'bootstrap5',

    # Local modules
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'api.apps.ApiConfig',
]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ahs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.all_urls',
                'core.context_processors.ahs_serialized_userdata',
            ],
        },
    },
]

ASGI_APPLICATION = 'ahs.asgi.application'


# Database

# DB_HOST and DB_PORT env vars must be None in order to connect over unix socket,
# which is faster (missing network stack).
#
# The DB container forwards host port 5433 to container port 5432 to be able to connect
# with a database manager without conflicting the port of a potential host postgresql database.
# django.db.backends.postgresql supports psycopg3 natively.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASS'),
        'HOST': environ.get('DB_HOST', None),
        'PORT': environ.get('DB_PORT', None),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/assets/'
STATICFILES_DIRS = [BASE_DIR / 'assets']


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'login'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'


AUTH_USER_MODEL = "accounts.AHSUser"

INTERNAL_IPS = [
    '127.0.0.1',
]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {name} {levelname} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'default': {
            'format': '%(asctime)s [%(levelname)s]- %(message)s',
        },
    },
    'handlers': {
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'ahs.log',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['rotating_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'webpack_bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["unix:///tmp/redis/redis.sock"],
        },
    },
}

# security related stuff
SESSION_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies
SESSION_COOKIE_HTTPONLY = True

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# enumerate container/host ip
# adds docker gateway ip to ALLOWED_HOSTS
if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    ipl = [ip[: ip.rfind(".")] + ".1" for ip in ips]
    INTERNAL_IPS += ipl
    ALLOWED_HOSTS += [hostname, '0.0.0.0'] + ipl

    SECURE_CONTENT_TYPE_NOSNIFF = False
    CORS_ORIGIN_ALLOW_ALL = True

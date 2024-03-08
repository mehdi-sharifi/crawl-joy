from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ["crawljoy.devsecworld.com","crawljoy-api-service"]
CSRF_TRUSTED_ORIGINS = ["http://crawljoy.devsecworld.com", "https://crawljoy.devsecworld.com", "http://crawljoy-api-service"]

THIRD_PARTY_APPS = [
    'rest_framework.authtoken',
    'rest_framework',
    'rest_framework_api_key',
    # 'drf_yasg',
]

LOCAL_APPS = [
    'api',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,

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

ROOT_URLCONF = 'crawlerproject.urls'

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

WSGI_APPLICATION = 'crawlerproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('CRAWLER_POSTGRES_DB'),
        'USER': os.environ.get('CRAWLER_POSTGRES_USER'),
        'PASSWORD': os.environ.get('CRAWLER_POSTGRES_PASSWORD'),
        'HOST': 'postgres-service',
        # 'PORT': '32432',
        'PORT': '5432',
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


STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SWAGGER_SETTINGS = {
#     'USE_SESSION_AUTH': False,
    
#     'SECURITY_DEFINITIONS': {
#         'api_key': {
#             'type': 'apiKey',
#             'in': 'header',
#             'name': 'Authorization'
#         }
#     },
#     'VALIDATOR_URL': None,

# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://redis-service:6379/1",
        # "LOCATION": f"redis://127.0.0.1:32379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

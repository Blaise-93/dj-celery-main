from pathlib import Path
import os
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# shared across the entire system
SHARED_APPS = [

    "daphne",
    'django_tenants',
    "profiles",
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # third party apps

    'django_celery_beat',
    'rest_framework',
    'mptt',
    "channels",
    "crispy_forms",
    'corsheaders',
    'crispy_bootstrap5',

]

# 2024-11-10 17:55:18.659813
if DEBUG:
    SHARED_APPS += [
        "django_browser_reload",  # Relaod automatically browser after changes
    ]

# are basically for the clients that works on the domain
TENANT_APPS = [
    # local apps

    "profiles",
    "customers",
    "products",
    "reports",
    "sales",
    'posts',
    'task1',
    "chatrooms",
    'inventory',
    'task2',
    "chats",
    "blogs",
    "blogs_api",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


]

INSTALLED_APPS = SHARED_APPS + \
    [app for app in TENANT_APPS if app not in SHARED_APPS]

# python manage.py runserver

MIDDLEWARE = [
   
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


]

ROOT_URLCONF = 'dj_celery.urls'

# use the public schema accept for the project url if it can't be found

PUBLIC_SCHEMA_URLCONFIG = 'app.urls'

# CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Restframework Permissions
# https://openfolder.sh/django-tutorial-as-you-type-search-with-ajax

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.IsAdminUser'
    ]
}

# Permissions
# AllowAny
# IsAuthenticated
# IsAdminUser
# IsAuthenticatedOrReadOnly

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

WSGI_APPLICATION = 'dj_celery.wsgi.application'

ASGI_APPLICATION = "dj_celery.asgi.application"
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql' , #ENUOHP,
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv("POSTGRES_NAME"),
        "USER": os.getenv('POSTGRES_USER'),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": int(os.getenv("POSTGRES_PORT"))
    }

}


AUTH_USER_MODEL = 'profiles.User'

DATABASE_ROUTERS = [
    'django_tenants.routers.TenantSyncRouter',
]

TENANT_MODEL = 'app.Client'

TENANT_DOMAIN_MODEL = 'app.Domain'

PUBLIC_SCHEMA_NAME = "public"

SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
TENANT_COLOR_ADMIN_APPS = True
AUTO_DROP_SCHEMA = True


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


CELERY_BEAT_SCHEDULE = {
    'scheduled_task': {
        "task": "posts.tasks.add",
        'schedule': 5.0,
        'args': (2, 50),
    },
    "database": {
        "task": "task2.tasks.bkup",
        "schedule": 5.0
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),
                    # BASE_DIR / "sales"/ "static",
                    ]
STATIC_ROOT = 'static_root'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TEMPLATE_DEBUG = True


# REDIS_CHANNEL CONFIG
CHANNEL_LAYERS = {
    'default': {
        # "BACKEND":"channels_redis.core.RedisChannelLayer",
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # "CONFIG": {
        #   "hosts": [(os.getenv('REDIS_URL'), os.getenv('REDIS_URL'))]
        # "hosts": [('127.0.0.1', 6379)]
        #  BACKEND":"channels_redis.core.InMemoryChannelLayer",
        # }
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# EMAIL CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


# https://ratedwap.com/cat/old/Downloads/movie/215.html


# Elastic search
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    }
}


CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000',
    'http://localhost:5173'
]


# <https://github.com/django-tenants/django-tenants>. :)

""" 
TENANT_SUBFOLDER_PREFIX = "clients"
In the example given above, the prefixed path ``/r`` will become ``/clients``.
e.g. http://www.mydomain.local/clients/schemaname/ instead of http://www.mydomain.
 """
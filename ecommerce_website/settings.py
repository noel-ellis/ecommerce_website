import os
from pathlib import Path

import environ

# reading .env file
env = environ.Env()
env.read_env(env.str('../', '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "corsheaders",
    "users.apps.UsersConfig",
    "store.apps.StoreConfig",
    "cart.apps.CartConfig",
    "wishlist.apps.WishlistConfig",
    "payment.apps.PaymentConfig",
    "orders.apps.OrdersConfig",
    "stripe",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "watson",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce_website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "wishlist.context_processors.wishlist"
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce_website.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'ecomm-db',
        'PORT': 5432,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_TEMPLATE_PACK = "bootstrap4"

AUTH_USER_MODEL = 'users.UserBase'
LOGIN_REDIRECT_URL = 'users:settings'
LOGIN_URL = 'users:login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("APP_EMAIL")
EMAIL_HOST_PASSWORD = env("APP_PASSWORD")

STRIPE_API_SECRET_KEY = env("STRIPE_API_SECRET_KEY")
STRIPE_ENDPOINT_SECRET = env("STRIPE_ENDPOINT_SECRET")

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://0.0.0.0:8000',
]
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://0.0.0.0:8000',
]
CORS_ALLOWED_ORIGINS = [
    "http://0.0.0.0:8000",
    "http://localhost:8000",
]
CORS_ALLOW_CREDENTIALS = True

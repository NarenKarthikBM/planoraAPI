import os

from .env import env

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
# setup()

# SITE_ROOT = root()

DEBUG = env.bool("DEBUG", default=True)
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]

SECRET_KEY = env.str(
    "SECRET_KEY",
    default="i)=y6havm=8y01$t8f&=!k^qc$kk29!$an3he^*zt!7-u4nnj^",
)

# ALLOWED_HOSTS = env.list("ALLOWED_HOSTS") or []
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users",
    "events",
]


# 'django.middleware.csrf.CsrfViewMiddleware',
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "users.CustomUser"

ROOT_URLCONF = "planoraAPI.urls"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": env.db_url(
        "DATABASE_URL",
        default="mysql://USER:PASSWORD@HOST:2000/NAME",
    ),
}

# DATABASES["default"]["OPTIONS"] = {"connect_timeout": 10}
WSGI_APPLICATION = "planoraAPI.wsgi.application"

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ADMINS = [x.split(":") for x in env.list("DJANGO_ADMINS", default="")]

AUTH_USER_MODEL = "users.CustomUser"


STATIC_URL = "/static/"
STATIC_ROOT = "static"


# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "django_s3_storage.storage.StaticS3Storage",
#     },
#     "default": {
#         "BACKEND": "django_s3_storage.storage.S3Storage",
#     },
# }

from decouple import config

# default backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("smtp.gmail.com", cast=str, default=None)
EMAIL_PORT = config("EMAIL_PORT", cast=str, default="587")  # Recommended
EMAIL_HOST_USER = config("planora3672@gmail.com", cast=str, default=None)
EMAIL_HOST_PASSWORD = config("ogbx eccp hijt vcel", cast=str, default=None)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default="True").lower() == "true"
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default="False").lower() == "true"

ADMIN_USER_NAME = config("ADMIN_USER_NAME", default="Admin user")
ADMIN_USER_EMAIL = config("ADMIN_USER_EMAIL", default=None)

MANAGERS = []
ADMINS = []
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS += [(f"{ADMIN_USER_NAME}", f"{ADMIN_USER_EMAIL}")]
    MANAGERS = ADMINS

ADMIN_USER_EMAIL = "nirman22@iiserb.ac.in"

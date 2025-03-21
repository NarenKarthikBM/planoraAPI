from planoraAPI.settings import env

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Use TLS for security
EMAIL_HOST_USER = env.str(
    "EMAIL_HOST_USER",
    default="name@gmail.com",
)
EMAIL_HOST_PASSWORD = env.str(
    "EMAIL_HOST_PASSWORD",
    default="password",
)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

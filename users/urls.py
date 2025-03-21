from django.urls import path

from . import views

users_api_v1_urls = [
    path(
        "obtain-auth-token/",
        views.UserObtainAuthTokenAPI().as_view(),
        name="user-obtain-auth-token",
    ),
    path(
        "register/",
        views.UserRegistrationAPI().as_view(),
        name="user-registration",
    ),
]

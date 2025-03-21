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
    path(
        "send-verification-otp/",
        views.UserSendVerificationOTPAPI().as_view(),
        name="user-send-verification-otp",
    ),
    path(
        "verify-otp/",
        views.UserVerifyOTPAPI().as_view(),
        name="user-verify-otp",
    ),
    path(
        "create-organisation/",
        views.OrganisationCreateAPI().as_view(),
        name="organisation-create",
    ),
    path(
        "organisation-list/",
        views.UserOrganisationListAPI().as_view(),
        name="user-organisation-list",
    ),
]

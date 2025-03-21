from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

from users.models import UserAuthTokens


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token, device_token = (
            request.META.get("HTTP_AUTHORIZATION"),
            request.META.get("HTTP_DEVICE_TOKEN"),
        )
        if not auth_token or not device_token:
            return None

        try:
            user_auth_token = UserAuthTokens.objects.get(
                auth_token=auth_token, device_token=device_token
            )
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        return (user_auth_token.user, None)

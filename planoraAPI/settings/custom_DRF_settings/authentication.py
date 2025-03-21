from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

from users.models import UserAuthTokens


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.META.get("HTTP_AUTHORIZATION")
        if not auth_token:
            return None

        try:
            user_auth_token = UserAuthTokens.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        return (user_auth_token.user, None)

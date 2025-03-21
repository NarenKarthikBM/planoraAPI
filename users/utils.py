import secrets

from users.models import (
    CustomUser,
    UserAccessTokens,
    UserAuthTokens,
    # UserVerificationOTP,
)
from users.serializers import UserSerializer


def generate_tokens():
    return {
        "auth_token": secrets.token_urlsafe(120),
        "device_token": secrets.token_urlsafe(16),
    }


def generate_otp():
    generateSecrets = secrets.SystemRandom()
    return generateSecrets.randint(100000, 999999)


def authorize_user(data):
    user = CustomUser.objects.filter(email=data["email"]).first()

    if not user:
        return None

    if not user.check_password(data["password"]):
        return {"error": "Invalid Password"}

    tokens = generate_tokens()

    UserAuthTokens(
        user=user,
        auth_token=tokens["auth_token"],
        device_token=tokens["device_token"],
        type="web",
    ).save()

    return {
        "tokens": tokens,
        "user_details": UserSerializer(user).details_serializer(),
    }


def revoke_tokens(auth_token, device_token):
    UserAccessTokens.objects.filter(
        auth_token=auth_token, device_token=device_token
    ).delete()


def create_user(email, name, password):
    user = CustomUser(
        email=email,
        name=name,
    ).save()
    user.set_password(password)
    user.save()

    return user


# def create_verification_otp(user, entity, entity_type):
#     otp = generate_otp()
#     UserVerificationOTP(
#         user=user, otp=otp, entity=entity, entity_type=entity_type
#     ).save()

#     return otp


# def verify_otp(user, otp):
#     return UserVerificationOTP.objects.filter(user=user, otp=otp).first()

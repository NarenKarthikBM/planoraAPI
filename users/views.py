from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from users.models import (
    CustomUser,
    Organisation,
    OrganisationCommittee,
    UserPreference,
    UserVerificationOTP,
)
from users.serializers import (
    OrganisationSerializer,
    UserPreferenceSerializer,
    UserSerializer,
)
from users.utils import authorize_user, create_verification_otp
from users.validator import (
    OrganisationCreateInputValidator,
    UserObtainAuthTokenInputValidator,
    UserPreferenceInputValidator,
    UserRegistrationInputValidator,
)
from utils.emails import send_verification_email


class UserObtainAuthTokenAPI(APIView):
    """API view to obtain auth tokens

    Methods:
        POST
    """

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """POST Method to generate and serve the auth tokens

        Input Serializer:
            - email
            - password

        Output Serializer:
            - tokens
            - User Serializer (details_serializer)

        Possible Outputs:
            - Errors
                - User not found (email field)
                - incorrect password (password field)
            - Successes
                - tokens and user details

        """

        validated_data = UserObtainAuthTokenInputValidator(
            request.data
        ).serialized_data()
        user_authorization = authorize_user(validated_data)

        if not user_authorization:
            raise ValidationError({"error": "user not found", "field": "email"})

        if "error" in user_authorization:
            raise ValidationError({"error": "incorrect password", "field": "password"})

        return Response(user_authorization, status=status.HTTP_200_OK)


class UserRegistrationAPI(APIView):
    """API view to register a user

    Methods:
        POST
    """

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """POST Method to register a user

        Input Serializer:
            - email
            - password
            - first_name
            - last_name

        Output Serializer:
            - tokens
            - User Serializer (details_serializer)

        Possible Outputs:
            - Errors
            - email already exists (email field)
            - Successes
            - tokens and user details

        """

        if CustomUser.objects.filter(email=request.data.get("email")).exists():
            raise ValidationError({"error": "Email already exists", "field": "email"})

        validated_data = UserRegistrationInputValidator(request.data).serialized_data()

        user = CustomUser(
            email=validated_data["email"],
            name=validated_data["name"],
            mobile_no=validated_data["mobile_no"],
            location=validated_data["location"],
            latitude=validated_data["latitude"],
            longitude=validated_data["longitude"],
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        user.save()
        user.set_password(validated_data["password"])
        user.save()

        user_authorization = authorize_user(validated_data)

        return Response(user_authorization, status=status.HTTP_201_CREATED)


class UserSendVerificationOTPAPI(APIView):
    """API view to send OTP for user verification

    Methods:
        POST
    """

    permission_classes = []

    def post(self, request):
        """POST Method to send OTP for user verification

        Input Serializer:
            - email

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
            - User not found (email field)
            - Successes
            - success message

        """

        otp = create_verification_otp(request.user.email)
        send_verification_email(request.user, otp)
        # send_registration_otp_mail(request.user.email, otp)

        return Response(
            {
                "success": "OTP sent",
                "user": UserSerializer(request.user).details_serializer(),
            },
            status=status.HTTP_200_OK,
        )


class UserVerifyOTPAPI(APIView):
    """API view to verify OTP for user verification

    Methods:
        POST
    """

    permission_classes = []

    def post(self, request):
        """POST Method to verify OTP for user verification

        Input Serializer:
            - email
            - otp

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
            - User not found (email field)
            - Incorrect OTP (otp field)
            - Successes
            - success message

        """

        otp = request.data.get("otp")

        user_otp = UserVerificationOTP.objects.filter(email=request.user.email).first()

        if not user_otp:
            raise ValidationError({"error": "OTP not found", "field": "otp"})

        if user_otp.otp != otp:
            raise ValidationError({"error": "Incorrect OTP", "field": "otp"})

        CustomUser.objects.filter(email=request.user.email).update(email_verified=True)

        return Response(
            {
                "success": "OTP verified",
                "user": UserSerializer(request.user).details_serializer(),
            },
            status=status.HTTP_200_OK,
        )


class UserListAPI(APIView):
    """API view to list all users

    Methods:
        GET
    """

    def get(self, request):
        """GET Method to list all users

        Output Serializer:
            - User Serializer (details_serializer)

        Possible Outputs:
            - Errors
            - None
            - Successes
            - list of users

        """

        users = CustomUser.objects.all()

        return Response(
            {
                "users": [
                    UserSerializer(user).condensed_details_serializer()
                    for user in users
                ]
            },
            status=status.HTTP_200_OK,
        )


class OrganisationCreateAPI(APIView):
    """API view to register an organisation

    Methods:
        POST
    """

    def post(self, request):
        """POST Method to register an organisation

        Input Serializer:
            - name
            - logo
            - description
            - location
            - email
            - tags

        Output Serializer:
            - tokens
            - Organisation Serializer (details_serializer)

        Possible Outputs:
            - Errors
            - email already exists (email field)
            - Successes
            - tokens and user details

        """

        if Organisation.objects.filter(name=request.data.get("name")).exists():
            raise ValidationError(
                {
                    "error": "Organisation with the same name already exists",
                    "field": "name",
                }
            )

        validated_data = OrganisationCreateInputValidator(
            request.data
        ).serialized_data()

        organisation = Organisation(
            name=validated_data["name"],
            # logo=validated_data["logo"],
            description=validated_data["description"],
            email=validated_data["email"],
            tags=validated_data["tags"],
            location=validated_data["location"],
        )
        organisation.save()

        OrganisationCommittee(
            user=request.user,
            organisation=organisation,
            designation="Founder",
            is_founder=True,
        ).save()

        return Response(
            {
                "success": "Organisation created",
                "organisation": OrganisationSerializer(
                    organisation
                ).details_serializer(),
            },
            status=status.HTTP_201_CREATED,
        )


class UserOrganisationListAPI(APIView):
    """API view to list organisations for a user

    Methods:
        GET
    """

    def get(self, request):
        """GET Method to list organisations for a user

        Output Serializer:
            - Organisation Serializer (details_serializer)

        Possible Outputs:
            - Errors
            - None
            - Successes
            - list of organisations
        """

        user = request.user
        organisation_committees = OrganisationCommittee.objects.filter(user=user)

        return Response(
            {
                "organisations": [
                    {
                        "details": OrganisationSerializer(
                            org_committee.organisation
                        ).details_serializer(),
                        "designation": org_committee.designation,
                    }
                    for org_committee in organisation_committees
                ]
            },
            status=status.HTTP_200_OK,
        )


class OrganisationCommitteeMemberListAPI(APIView):
    """API view to list committee members of an organisation

    Methods:
        GET
    """

    def get(self, request, organisation_id):
        """GET Method to list committee members of an organisation

        Output Serializer:
            - User Serializer (condensed_details_serializer)

        Possible Outputs:
            - Errors
                - Organisation not found (organisation_id field)
            - Successes
                - list of committee members
        """

        organisation = Organisation.objects.filter(id=organisation_id).first()

        if not organisation:
            raise ValidationError(
                {"error": "Organisation not found", "field": "organisation_id"}
            )

        committee_members = OrganisationCommittee.objects.filter(
            organisation=organisation
        )

        return Response(
            {
                "committee_members": [
                    {
                        "user": UserSerializer(
                            member.user
                        ).condensed_details_serializer(),
                        "designation": member.designation,
                        "is_founder": member.is_founder,
                    }
                    for member in committee_members
                ]
            },
            status=status.HTTP_200_OK,
        )


class OrganisationAddCommitteeMemberAPI(APIView):
    """API view to add a committee member to an organisation

    Methods:
        POST
    """

    def post(self, request):
        """POST Method to add a committee member to an organisation

        Input Serializer:
            - organisation_id
            - user_id

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
            - Organisation not found (organisation_id field)
            - User not found (user_id field)
            - Successes
            - success message

        """

        organisation_id = request.data.get("organisation_id")
        committee_members = request.data.get("committee_members")
        users = []

        organisation = Organisation.objects.filter(id=organisation_id).first()

        if not organisation:
            raise ValidationError(
                {"error": "Organisation not found", "field": "organisation_id"}
            )

        for committee_member in committee_members:
            user = CustomUser.objects.filter(id=committee_member["user_id"]).first()
            designation = committee_member["designation"]

            if not user:
                raise ValidationError(
                    {
                        "error": "User not found",
                        "field": "user_id",
                        "user_id": committee_member["user_id"],
                    }
                )

            if user in organisation.committee.all():
                continue

            if isinstance(designation, str) and len(designation) == 0:
                designation = None

            users.append({"user": user, "designation": committee_member["designation"]})

        for user in users:
            OrganisationCommittee(
                user=user, organisation=organisation, designation=designation
            ).save()

        return Response(
            {
                "success": "Committee member added",
                "organisation": organisation.name,
                "committee": [
                    UserSerializer(user).condensed_details_serializer()
                    for user in users
                ],
            },
            status=status.HTTP_200_OK,
        )


class OrganisationRemoveCommitteeMemberAPI(APIView):
    """API view to remove a committee member from an organisation

    Methods:
        POST
    """

    def post(self, request):
        """POST Method to remove a committee member from an organisation

        Input Serializer:
            - organisation_id
            - user_id

        Output Serializer:
            - success message

        Possible Outputs:
            - Errors
            - Organisation not found (organisation_id field)
            - User not found (user_id field)
            - Successes
            - success message

        """

        organisation_id = request.data.get("organisation_id")
        user_id = request.data.get("user_id")

        organisation = Organisation.objects.filter(id=organisation_id).first()
        user = CustomUser.objects.filter(id=user_id).first()

        if not user:
            raise ValidationError(
                {"error": "User not found", "field": "user_id", "user_id": user_id}
            )

        if not organisation:
            raise ValidationError(
                {"error": "Organisation not found", "field": "organisation_id"}
            )

        OrganisationCommittee.objects.filter(
            user=user, organisation=organisation
        ).delete()

        return Response(
            {
                "success": "Committee member removed",
                "organisation": organisation.name,
                "removed_user": UserSerializer(user).condensed_details_serializer(),
            },
            status=status.HTTP_200_OK,
        )


class UserPreferenceRetrieveAPI(APIView):
    """API view to retrieve user preferences"""

    def get(self, request):
        """GET Method to retrieve user preferences

        Output Serializer:
            - UserPreference Serializer (details_serializer)

        Possible Outputs:
            - Errors
                - User preferences not found (field: user)
            - Successes
                - User preferences data
        """

        user = request.user  # Assuming authentication is used
        user_preferences = UserPreference.objects.filter(user=user).first()

        if not user_preferences:
            raise ValidationError(
                {"error": "User preferences not found", "field": "user"}
            )

        return Response(
            {"preferences": UserPreferenceSerializer(user_preferences).data},
            status=status.HTTP_200_OK,
        )


class UserPreferenceUpdateAPI(APIView):
    """API view to update user preferences"""

    def post(self, request):
        """POST Method to update user preferences

        Input Serializer:
            - designation
            - preferred_categories
            - allow_marketing_emails
            - allow_event_updates
            - allow_system_notifications

        Output Serializer:
            - Updated user preferences

        Possible Outputs:
            - Errors
                - Invalid data fields
            - Successes
                - Updated preferences
        """

        user = request.user

        validated_data = UserPreferenceInputValidator(request.data).serialized_data()

        # Retrieve or create user preferences
        user_preferences, created = UserPreference.objects.get_or_create(user=user)

        # Update fields
        user_preferences.designation = validated_data["designation"]
        user_preferences.preferred_categories = validated_data["preferred_categories"]
        user_preferences.allow_marketing_emails = validated_data[
            "allow_marketing_emails"
        ]
        user_preferences.allow_event_updates = validated_data["allow_event_updates"]
        user_preferences.allow_system_notifications = validated_data[
            "allow_system_notifications"
        ]

        user_preferences.save()

        return Response(
            {
                "success": "User preferences updated",
                "preferences": UserPreferenceSerializer(user_preferences).data,
            },
            status=status.HTTP_200_OK,
        )

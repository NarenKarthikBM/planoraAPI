from utils.datetime import serialize_datetime

from . import models


class UserSerializer:
    """This serializer class contains serialization methods for User Model"""

    def __init__(self, obj: models.CustomUser):
        self.obj = obj

    def details_serializer(self):
        """This serializer method serializes all fields of the User model

        Returns:
            dict: Dictionary of all details
        """

        return {
            "id": self.obj.id,
            "name": self.obj.name,
            "email": self.obj.email,
            "email_verified": self.obj.email_verified,
            "location": self.obj.location,
            "latitude": self.obj.latitude,
            "longitude": self.obj.longitude,
            "mobile_no": self.obj.mobile_no,
            "is_active": self.obj.is_active,
            "is_staff": self.obj.is_staff,
            "is_superuser": self.obj.is_superuser,
            "date_joined": serialize_datetime(self.obj.date_joined),
        }

    def condensed_details_serializer(self):
        """This serializer method serializes all descriptive fields of the User model

        Returns:
            dict: Dictionary of all user descriptive details
        """

        return {
            "id": self.obj.id,
            "email": self.obj.email,
            "name": self.obj.name,
        }


class OrganisationSerializer:
    """This serializer class contains serialization methods for Organisation Model"""

    def __init__(self, obj: models.Organisation):
        self.obj = obj

    def details_serializer(self):
        """This serializer method serializes all fields of the Organisation model

        Returns:
            dict: Dictionary of all details
        """

        return {
            "id": self.obj.id,
            "name": self.obj.name,
            "description": self.obj.description,
            "email": self.obj.email,
            "tags": self.obj.tags,
            "location": self.obj.location,
            "created_at": serialize_datetime(self.obj.created_at),
            "updated_at": serialize_datetime(self.obj.updated_at),
        }

    def condensed_details_serializer(self):
        """This serializer method serializes all descriptive fields of the Organisation model

        Returns:
            dict: Dictionary of all organisation descriptive details
        """

        return {
            "id": self.obj.id,
            "name": self.obj.name,
            "description": self.obj.description,
            "location": self.obj.location,
        }


class UserPreferenceSerializer:
    """This serializer class contains serialization methods for UserPreference Model"""

    def __init__(self, obj: models.UserPreference):
        self.obj = obj

    def details_serializer(self):
        """This serializer method serializes all fields of the UserPreference model

        Returns:
            dict: Dictionary of all details
        """

        return {
            "id": self.obj.id,
            "user": UserSerializer(self.obj.user).condensed_details_serializer(),
            "designation": self.obj.designation,
            "preferred_category": self.obj.preferred_categories,
            "allow_marketing_emails": self.obj.allow_marketing_emails,
            "allow_event_updates": self.obj.allow_event_updates,
            "allow_system_notifications": self.obj.allow_system_notifications,
            "created_at": self.obj.created_at,
            "updated_at": self.obj.updated_at,
        }

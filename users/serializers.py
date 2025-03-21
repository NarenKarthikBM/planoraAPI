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
            "role": self.obj.role,
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
            "latitude": self.obj.latitude,
            "longitude": self.obj.longitude,
            "created_by": UserSerializer(
                self.obj.created_by
            ).condensed_details_serializer(),
            "updated_by": UserSerializer(
                self.obj.updated_by
            ).condensed_details_serializer(),
            "created_at": serialize_datetime(self.obj.created_at),
            "updated_at": serialize_datetime(self.obj.updated_at),
        }

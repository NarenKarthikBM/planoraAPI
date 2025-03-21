from users.serializers import UserSerializer

from . import models


class EventSerializer:
    """This serializer class contains serialization methods for Event Model"""

    def __init__(self, obj: models.Event):
        self.obj = obj

    def details_serializer(self):
        """This serializer method serializes all fields of the User model

        Returns:
            dict: Dictionary of all details
        """

        return {
            "id": self.obj.id,
            "name": self.obj.name,
            "description": self.obj.description,
            "start_datetime": self.obj.start_datetime,
            "end_datetime": self.obj.end_datetime,
            "category": self.obj.category,
            "tags": self.obj.tags,
            "type": self.obj.type,
            "location": self.obj.location,
            "latitude": self.obj.latitude,
            "longitude": self.obj.longitude,
            "status": self.obj.status,
            "created_by": UserSerializer(
                self.obj.created_by.id
            ).condensed_details_serializer(),
            "updated_by": UserSerializer(
                self.obj.updated_by.id
            ).condensed_details_serializer(),
            "created_at": self.obj.created_at,
            "updated_at": self.obj.updated_at,
        }

    def get_scan_id(self):
        return self.obj.scan_id


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
            "user": UserSerializer(
                self.obj.user
            ).condensed_details_serializer(),
            "designation": self.obj.designation,
            "preferred_category": self.obj.preferred_categories,
            "allow_marketing_emails": self.obj.allow_marketing_emails,
            "allow_event_updates": self.obj.allow_event_updates,
            "allow_system_notifications": self.obj.allow_system_notifications,
            "created_at": self.obj.created_at,
            "updated_at": self.obj.updated_at,
        }
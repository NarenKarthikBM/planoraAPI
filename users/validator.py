from utils.validator import GeneralValidator


class UserObtainAuthTokenInputValidator(GeneralValidator):
    def __init__(self, data) -> None:
        self.data = data

    def serialized_data(self):
        email, password = self.data.get("email"), self.data.get("password")
        return {
            "email": self.validate_data(
                email,
                self.validate_type("Email", email, str)
                or self.validate_contains("Email", email, ["@"]),
                "email",
            ),
            "password": self.validate_data(
                password, self.validate_type("Password", password, str), "password"
            ),
        }


class UserRegistrationInputValidator(GeneralValidator):
    def __init__(self, data) -> None:
        self.data = data

    def serialized_data(self):
        email, name, password, location, lattitude, longitude, mobile_no = (
            self.data.get("email"),
            self.data.get("name"),
            self.data.get("password"),
            self.data.get("location"),
            self.data.get("latitude"),
            self.data.get("longitude"),
            self.data.get("mobile_no"),
        )
        return {
            "email": self.validate_data(
                email,
                self.validate_type("Email", email, str)
                or self.validate_contains("Email", email, ["@"]),
                "email",
            ),
            "name": self.validate_data(
                name, self.validate_type("Name", name, str), "name"
            ),
            "password": self.validate_data(
                password, self.validate_type("Password", password, str), "password"
            ),
            "location": self.validate_data(
                location,
                self.validate_type("Location", location, str),
                "location",
            ),
            "latitude": self.validate_data(
                lattitude,
                self.validate_type("Latitude", lattitude, float) if lattitude else None,
                "latitude",
            ),
            "longitude": self.validate_data(
                longitude,
                self.validate_type("Longitude", longitude, float)
                if longitude
                else None,
                "longitude",
            ),
            "mobile_no": self.validate_data(
                mobile_no,
                self.validate_type("Mobile No", mobile_no, str) if mobile_no else None,
                "mobile_no",
            ),
        }


class OrganisationCreateInputValidator(GeneralValidator):
    def __init__(self, data) -> None:
        self.data = data

    def serialized_data(self):
        name, email, location, tags, description = (
            self.data.get("name"),
            self.data.get("email"),
            self.data.get("location"),
            self.data.get("tags"),
            self.data.get("description"),
        )
        return {
            "name": self.validate_data(
                name, self.validate_type("Name", name, str), "name"
            ),
            "email": self.validate_data(
                email,
                self.validate_type("Email", email, str)
                or self.validate_contains("Email", email, ["@"]),
                "email",
            ),
            "location": self.validate_data(
                location,
                self.validate_type("Location", location, str) if location else None,
                "location",
            ),
            "tags": self.validate_data(
                tags,
                self.validate_type("Tags", tags, list) if tags else None,
                "tags",
            ),
            "description": self.validate_data(
                description,
                self.validate_type("Description", description, str)
                if description
                else None,
                "description",
            ),
        }

class UserPreferenceValidator(GeneralValidator):
    def __init__(self, data):
        self.data = data

    def serialized_data(self):
        return {
            "user": self.validate_data(self.data.get("user")),
            "designation": self.validate_data(
                self.data.get("designation"),
                self.validate_type("designation", self.data.get("designation"), str),
            ),
            "preferred_categories": self.validate_data(
                self.data.get("preferred_categories"),
                self.validate_choices(
                    "preferred_categories",
                    self.data.get("preferred_categories"),
                    self.categories,  # Must be defined elsewhere
                ),
            ),
            "allow_marketing_emails": self.validate_data(
                self.data.get("allow_marketing_emails"),
                self.validate_type("allow_marketing_emails", self.data.get("allow_marketing_emails"), bool),
            ),
            "allow_event_updates": self.validate_data(
                self.data.get("allow_event_updates"),
                self.validate_type("allow_event_updates", self.data.get("allow_event_updates"), bool),
            ),
            "allow_system_notifications": self.validate_data(
                self.data.get("allow_system_notifications"),
                self.validate_type("allow_system_notifications", self.data.get("allow_system_notifications"), bool),
            ),
        }
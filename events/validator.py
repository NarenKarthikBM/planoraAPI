from users.utils import generate_scan_id
from utils.validator import GeneralValidator


class EventCreateInputValidator(GeneralValidator):
    def __init__(self, data) -> None:
        self.data = data

    def serialized_data(self):
        return {
            "name": self.validate_data(
                self.data.get("name"),
                self.validate_type("name", self.data.get("name"), str),
            ),
            "scan_id": str(generate_scan_id()),
            "description": self.validate_data(
                self.data.get("description"),
                self.validate_type("description", self.data.get("description"), str),
            ),
            "start_datetime": self.validate_data(
                self.data.get("start_datetime"),
                self.validate_type(
                    "start_datetime", self.data.get("start_datetime"), str
                ),
            ),
            "end_datetime": self.validate_data(
                self.data.get("end_datetime"),
                self.validate_type("end_datetime", self.data.get("end_datetime"), str),
            ),
            "category": self.validate_data(
                self.data.get("category"),
                self.validate_type("category", self.data.get("category"), str),
            ),
            "tags": self.validate_data(
                self.data.get("tags") or [],
                self.validate_type("tags", self.data.get("tags"), list),
            ),
            "type": self.validate_data(
                self.data.get("type"),
                self.validate_type("type", self.data.get("type"), str)
                or self.validate_choices(
                    "type", self.data.get("type"), ["online", "offline", "hybrid"]
                ),
            ),
            "location": self.validate_data(
                self.data.get("location"),
                self.validate_type("location", self.data.get("location"), str),
            ),
            "latitude": self.validate_data(
                self.data.get("latitude"),
                self.validate_type("latitude", self.data.get("latitude"), str),
            ),
            "longitude": self.validate_data(
                self.data.get("longitude"),
                self.validate_type("longitude", self.data.get("longitude"), str),
            ),
        }

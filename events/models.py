from django.db import models
from django.utils.translation import gettext_lazy as _

type_choices = [("online", "Online"), ("offline", "Offline"), ("hybrid", "Hybrid")]
categories = [
    ("music", "Music"),
    ("nightlife", "Nightlife"),
    ("concert", "Concert"),
    ("holidays", "Holidays"),
    ("dating", "Dating"),
    ("hobbies", "Hobbies"),
    ("coding", "Coding"),
    ("others", "Others"),
    ("business", "Business"),
    ("food_drink", "Food & Drink"),
]


class Event(models.Model):
    """This model stores the details of events

    Returns:
        class: details of events
    """

    organisation = models.ForeignKey(
        "users.Organisation",
        verbose_name=_("organisation"),
        help_text="Organisation",
        on_delete=models.CASCADE,
        related_name="events",
    )
    name = models.CharField(_("name"), help_text="Name", max_length=255)
    scan_id = models.CharField(_("scan id"), help_text="Scan ID", max_length=10)
    description = models.TextField(_("description"), help_text="Description")
    start_datetime = models.DateTimeField(
        _("start datetime"), help_text="Start Datetime"
    )
    end_datetime = models.DateTimeField(_("end datetime"), help_text="End Datetime")
    category = models.CharField(
        _("category"), help_text="Category", max_length=50, choices=categories
    )
    tags = models.JSONField(_("tags"), help_text="Tags")
    type = models.CharField(
        _("type"), help_text="Type", max_length=255, choices=type_choices
    )
    location = models.CharField(_("location"), help_text="Location", max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)
    status = models.CharField(
        _("status"),
        help_text="Status",
        max_length=255,
        choices=[
            ("draft", "Draft"),
            ("published", "Published"),
            ("canceled", "Canceled"),
        ],
    )
    attendees = models.ManyToManyField(
        "users.CustomUser",
        through="events.EventAttendees",
    )

    created_by = models.ForeignKey(
        "users.CustomUser",
        verbose_name=_("created by"),
        help_text="Created By",
        on_delete=models.CASCADE,
        related_name="events_created",
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), help_text="Updated At", auto_now=True
    )

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.name


class EventNotificationConfig(models.Model):
    """This model stores the details of event notification configuration

    Returns:
        class: details of event notification configuration
    """

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        verbose_name="event",
        help_text="Event",
        related_name="notification_config",
    )
    notification_config = models.JSONField(
        _("notification config"), help_text="Notification Config"
    )
    reminder_mail_sent = models.BooleanField(
        _("reminder mail sent"), help_text="reminder mail sent", default=False
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), help_text="Updated At", auto_now=True
    )

    class Meta:
        verbose_name = _("Event Notification Config")
        verbose_name_plural = _("Event Notification Configs")

    def __str__(self):
        return self.event.name


class EventAttendees(models.Model):
    """This model stores the details of event attendees

    Returns:
        class: details of event attendees
    """

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        verbose_name="event",
        help_text="Event",
        related_name="event_attendees",
    )
    attendee = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="attendee",
        help_text="Attendee",
        related_name="events_attended",
    )
    is_present = models.BooleanField(
        _("is present"), help_text="Is Present", default=False
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), help_text="Updated At", auto_now=True
    )

    class Meta:
        verbose_name = _("Event Attendee")
        verbose_name_plural = _("Event Attendees")

    def __str__(self):
        return f"{self.event.name} - {self.attendee.name}"


class EventInteractions(models.Model):
    """This model stores the details of event interactions

    Returns:
        class: details of event interactions
    """

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        verbose_name="event",
        help_text="Event",
        related_name="interactions",
    )
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="User",
        related_name="events_interactions",
    )
    interaction_type = models.CharField(
        _("interaction type"),
        help_text="Interaction Type",
        max_length=255,
        choices=[
            ("like", "Like"),
            ("comment", "Comment"),
            ("share", "Share"),
            ("view", "View"),
        ],
    )
    interaction_data = models.JSONField(
        _("interaction data"), help_text="Interaction Data"
    )
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )

    class Meta:
        verbose_name = _("Event Interaction")
        verbose_name_plural = _("Event Interactions")

    def __str__(self):
        return f"{self.event.name} - {self.user.name}"


class EventFeedback(models.Model):
    """This model stores the details of event feedback

    Returns:
        class: details of event feedback
    """

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        verbose_name="event",
        help_text="Event",
        related_name="feedback",
    )
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="User",
        related_name="events_feedback",
    )
    rating = models.FloatField(_("rating"), help_text="Rating")
    feedback = models.TextField(_("feedback"), help_text="Feedback")
    created_at = models.DateTimeField(
        _("created at"), help_text="Created At", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), help_text="Updated At", auto_now=True
    )

    class Meta:
        verbose_name = _("Event Feedback")
        verbose_name_plural = _("Event Feedbacks")

    def __str__(self):
        return f"{self.event.name} - {self.user.name}"

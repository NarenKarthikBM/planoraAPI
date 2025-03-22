from django.contrib import admin

from .models import (
    Event,
    EventAttendees,
    EventFeedback,
    EventInteractions,
    EventNotificationConfig,
)

admin.site.register(Event)
admin.site.register(EventNotificationConfig)
admin.site.register(EventAttendees)
admin.site.register(EventInteractions)
admin.site.register(EventFeedback)

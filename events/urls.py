from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

events_api_v1_urls = [
    path(
        "public-feed/",
        views.EventsPublicFeedAPI().as_view(),
        name="events-public-feed",
    ),
    path(
        "personalised-feed/",
        views.EventsFeedAPI().as_view(),
        name="events-personalised-feed",
    ),
    path(
        "organisation-event-list/<int:organisation_id>/",
        views.EventListByOrganisation().as_view(),
        name="events-list-by-organisation",
    ),
    path(
        "create/<int:organisation_id>/",
        views.EventCreateAPI().as_view(),
        name="events-create",
    ),
    path(
        "details/<int:event_id>/",
        views.EventDetailAPI().as_view(),
        name="events-details",
    ),
    path(
        "edit/<int:event_id>/",
        views.EventEditAPI().as_view(),
        name="events-edit-details",
    ),
    path(
        "publish/<int:event_id>/",
        views.EventPublishAPI().as_view(),
        name="events-publish",
    ),
    path(
        "rsvp/<int:event_id>/",
        views.EventRSVPAPI().as_view(),
        name="events-rsvp",
    ),
    path(
        "check-user-interactions/<int:event_id>/",
        views.EventCheckUserInteractionsAPI().as_view(),
        name="events-check-user-interactions",
    ),
    path(
        "event-list-by-user/",
        views.EventsListByUserAPI().as_view(),
        name="event-list-by-user",
    ),
]

# Adding media URLs inside events API (Not recommended)
if settings.DEBUG:
    events_api_v1_urls += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

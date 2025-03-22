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
]

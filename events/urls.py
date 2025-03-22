from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
]

# Adding media URLs inside events API (Not recommended)
if settings.DEBUG:
    events_api_v1_urls += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
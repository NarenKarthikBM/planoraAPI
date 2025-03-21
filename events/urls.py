from django.urls import path

from . import views
from django.urls import path
from utils.qr_generator import serve_qr

urlpatterns = [
    path('<int:event_id>/qr/', serve_qr, name="event_qr"),
]

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

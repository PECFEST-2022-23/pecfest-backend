from django.urls import path
from knox import views as knox_views

from events.views import EventAPIView, EventRegistrationAPIView

urlpatterns = [
    path("", EventAPIView.as_view(), name="get"),
    path("register/", EventRegistrationAPIView.as_view(), name="event_registration"),
    path(
        "<str:event_id>/register/",
        EventRegistrationAPIView.as_view(),
        name="event_registration",
    ),
]

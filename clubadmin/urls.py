from django.urls import path
from clubadmin.views import EventAPIView, ParticipantsAPIView
urlpatterns = [
    path(
        "event/",
        EventAPIView.as_view(),
        name="add_event",
    ),
    path(
        "event/<str:event_id>",
        EventAPIView.as_view(),
        name = "edit_event"
    ),
    path(
        "event/<str:event_id>/participants",
        ParticipantsAPIView.as_view(),
        name = "event participants"
    )
]
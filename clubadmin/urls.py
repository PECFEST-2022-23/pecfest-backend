from django.urls import path
from clubadmin.views import EventAPIView, ParticipantsAPIView

urlpatterns = [
    path("<str:club_id>/", EventAPIView.as_view(), name="get_event_by_club_id"),
    path(
        "",
        EventAPIView.as_view(),
        name="add_event",
    ),
    path("<str:event_id>", EventAPIView.as_view(), name="edit_event"),
    path("<str:event_id>/participants", ParticipantsAPIView.as_view(), name = "event_participants")
]

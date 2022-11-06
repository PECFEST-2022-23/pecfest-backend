from django.urls import path

from events.views import (
    EventAPIView,
    MemberRegisterAPIView,
    TeamDetailsAPIView,
    TeamRegistrationAPIView,
)

urlpatterns = [
    path("", EventAPIView.as_view(), name="get"),
    path("<str:event_id>/", EventAPIView.as_view(), name="get_id"),
    path(
        "register/<str:event_id>/",
        TeamRegistrationAPIView.as_view(),
        name="team_registration",
    ),
    path(
        "add/<str:team_id>/",
        MemberRegisterAPIView.as_view(),
        name="member_registration",
    ),
    path(
        "<str:event_id>/team/",
        TeamDetailsAPIView.as_view(),
        name="team_details_from_event_id",
    ),
]

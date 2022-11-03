from django.urls import path
from knox import views as knox_views

from events.views import EventAPIView, MemberRegisterAPIView, TeamRegistrationAPIView

urlpatterns = [
    path("", EventAPIView.as_view(), name="get"),
    path(
        "<str:event_id>/register/",
        TeamRegistrationAPIView.as_view(),
        name="team_registration",
    ),
    path(
        "<str:team_id>/register/",
        MemberRegisterAPIView.as_view(),
        name="member_registration",
    ),
]

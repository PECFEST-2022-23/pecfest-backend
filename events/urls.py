from django.urls import path
from knox import views as knox_views

from events.views import EventAPIView, EventRegistrationAPIView, MemberRegisterAPIView

urlpatterns = [
    path("", EventAPIView.as_view(), name="get"),
    path("register/", EventRegistrationAPIView.as_view(), name="event_registration"),
    path(
        "<str:team_id>/register/",
        MemberRegisterAPIView.as_view(),
        name="member_registration",
    ),
]

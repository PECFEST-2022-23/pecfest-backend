from django.urls import path
from clubadmin.views import EventAPIView
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
    )
]
from django.urls import path

from clubadmin.views import EventAPIView

urlpatterns = [
    path("", EventAPIView.as_view(), name="create_get_event"),
    path("<str:event_id>/", EventAPIView.as_view(), name="edit_delete_event"),
]

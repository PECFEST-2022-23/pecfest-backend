from django.urls import path
from knox import views as knox_views

from events.views import EventAPIView

urlpatterns = [
    path("", EventAPIView.as_view(), name="get"),
]

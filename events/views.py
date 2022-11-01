from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Event
from .serializers import EventSerializer


class EventAPIView(GenericAPIView):
    events = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()

    def get(self, request):
        serializer = EventSerializer(self.events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        event_name = request.data.get("event")
        obj = Event.objects.filter(name=event_name)
        data = {"event": obj}
        return Response(data, status=status.HTTP_200_OK)

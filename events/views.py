from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from events.models import Event
from events.serializers import EventSerializer, TeamSerializer


class EventAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get(self, request, *args, **kwargs):
        event_objs = Event.objects.all()
        serializer = self.get_serializer(event_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request, *args, **kwargs):
    #     event_data = request.data.get("event")

    #     serializer = self.get_serializer(data=event_data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class EventRegistrationAPIView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = TeamSerializer

    def post(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        user_id = request.user.id

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            data = {"message": serializer.errors}
            return Response(data, status.HTTP_409_CONFLICT)

        data = {"message": event_id}
        return Response(data, status.HTTP_201_CREATED)

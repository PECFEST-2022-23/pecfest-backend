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

    def post(self, request, event_id, *args, **kwargs):
        user_id = request.user.id
        if "team_name" in request.data:
            team_name = request.data["team_name"]
        else:
            team_name = None

        serializer = self.get_serializer(
            data={"event_id": event_id, "team_name": team_name}
        )
        if serializer.is_valid():
            serializer.save()
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)

        data = {"message": "Registered Successfully"}
        data["id"] = serializer.data["id"]
        return Response(data, status.HTTP_201_CREATED)

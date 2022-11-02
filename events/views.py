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
        user_id = "a9f1e6e2-ab39-491a-b578-315c5c3c4715"  # to be deleted
        if "team_name" in request.data:
            team_name = request.data["team_name"]
        else:
            team_name = None

        serializer = self.get_serializer(
            data={"event_id": event_id, "team_name": team_name},
            context={"user": request.user},
        )
        if serializer.is_valid():
            serializer.save()
        else:
            data = serializer.errors
            return Response(data, status.HTTP_400_BAD_REQUEST)

        data = {"message": "Registered Successfully"}
        data["id"] = serializer.data["id"]
        return Response(data, status.HTTP_201_CREATED)


class EventUnregisterAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TeamSerializer

    def post(self, request, event_id, *args, **kwargs):
        user_id = request.user.id


# todo
# check if already registered - almost done - just need to change few lines in serializer
# create unregister api

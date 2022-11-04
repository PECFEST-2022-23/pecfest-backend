from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from events.models import Event
from events.serializers import EventSerializer, TeamMembersSerializer, TeamSerializer


class EventAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            event_id = request.GET["id"]
            event_objs = Event.objects.filter(id=event_id)
            serializer = self.get_serializer(event_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            event_objs = Event.objects.all()
            serializer = self.get_serializer(event_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TeamRegistrationAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamSerializer

    def post(self, request, event_id, *args, **kwargs):
        team_name = request.data.get("team_name")

        serializer = self.get_serializer(
            data={"event_id": event_id, "team_name": team_name},
            context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)

        data = {"message": "Registered Successfully"}
        data["id"] = serializer.data["id"]
        return Response(data, status.HTTP_201_CREATED)


class MemberRegisterAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamMembersSerializer

    def post(self, request, team_id, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data={"team_id": team_id, "user_id": user_id})

        serializer.is_valid(raise_exception=True)

        data = {"message": "Registered Successfully"}
        return Response(data, status.HTTP_200_OK)

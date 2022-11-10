from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from events.models import Event, Team, TeamMembers
from events.serializers import EventSerializer, TeamMembersSerializer, TeamSerializer
from events.utils import TeamUtil


class EventAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get("event_id")
        if event_id:
            try:
                event_obj = Event.objects.filter(id=event_id).first()
            except Exception:
                return Response(
                    {"message": "Invalid event id"}, status=status.HTTP_400_BAD_REQUEST
                )

            if event_obj:
                serializer = self.get_serializer(event_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Invalid event id"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            event_objs = Event.objects.all()
            serializer = self.get_serializer(event_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TeamRegistrationAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamSerializer

    def post(self, request, event_id, *args, **kwargs):
        team_name = request.data.get("team_name")

        if TeamMembers.objects.filter(
            team__event_id=event_id, user=request.user
        ).exists():
            return Response(
                {"message": "Already registered for this event"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data={"event_id": event_id, "team_name": team_name},
            context={"user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        team_obj = serializer.save()

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
        try:
            serializer.save()
        except Exception as e:
            return Response(
                {"message": "Already registered"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {"message": "Registered Successfully"}
        return Response(data, status.HTTP_200_OK)

    def delete(self, request, team_id, *args, **kwargs):
        try:
            teammember_obj = TeamMembers.objects.get(team_id=team_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Member not registered"}, status=status.HTTP_400_BAD_REQUEST
            )

        teammember_obj.delete()

        return Response({"message": "Member Removed"}, status=status.HTTP_200_OK)


class TeamDetailsAPIView(GenericAPIView, TeamUtil):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get("event_id")
        user = request.user
        try:
            t = user.teams.get(team__event_id=event_id)
        except Exception:
            return Response({"is_registered": False}, status.HTTP_200_OK)

        if t.team.event.type == "TEAM":
            response = {"team_name": t.team.name}
            response["id"] = t.team.id
            response["is_registered"] = True
            response[
                "team_valid"
            ] = t.team.is_registered  # if min and max size are fulfilled
            response["members"] = self.get_participants_json_from_team(t.team)
            response["event_type"] = t.team.event.type
            return Response(response, status.HTTP_200_OK)
        else:
            response = {}
            response["is_registered"] = True
            response["id"] = t.team.id
            response["members"] = self.get_participants_json_from_team(t.team)
            response["event_type"] = t.team.event.type
            return Response(response, status.HTTP_200_OK)


class TeamAPIView(GenericAPIView, TeamUtil):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        team_id = kwargs.get("team_id")
        try:
            team = Team.objects.get(id=team_id)
        except Exception:
            return Response(
                {"message": "Invalid Team ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        if team.event.type == "TEAM":
            response = {"team_name": team.name}
            response["id"] = team.id
            response["is_registered"] = True
            response[
                "team_valid"
            ] = team.is_registered  # if min and max size are fulfilled
            response["members"] = self.get_participants_json_from_team(team)
            response["event_type"] = team.event.type
            return Response(response, status.HTTP_200_OK)
        else:
            response = {}
            response["is_registered"] = True
            response["id"] = team.id
            response["members"] = self.get_participants_json_from_team(team)
            response["event_type"] = team.event.type
            return Response(response, status.HTTP_200_OK)

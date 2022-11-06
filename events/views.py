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


class TeamDetailsAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer

    # utility function to return list of users in a team -> works for both team and individual event
    def get_participants_json_from_team(self, t):
        participants = []
        for u in list(t.user.all()):
            participant = {
                "user_id":u.user.id,
                "first_name":u.user.first_name,
                "last_name":u.user.last_name,
                "email":u.user.email,
            }
            for d in list(u.user.details.all()):
                participant['college'] = d.college
                participant['mobile'] = d.mobile
                break

            participants.append(participant)

        return participants

    def get(self, request, event_id, *args, **kwargs):
        #user = request.user
        from events.models import User
        user = list(User.objects.filter(email = 'utkarshgoel.bt19cse@pec.edu.in'))[0]
        user_teams = list(user.teams.all())
        for t in user_teams:
            if str(t.team.event.id) == event_id:
                if t.team.event.type == "TEAM":
                    response = {"team_name":t.team.name}
                    response['is_registered'] = t.team.is_registered
                    response['members'] = self.get_participants_json_from_team(t.team)
                    return Response(response, status.HTTP_200_OK)
                else:
                    response = {"error":"not a team event"}
                    return Response(response, status.HTTP_400_BAD_REQUEST)
        
        return Response({"error":"not registered for this event"}, status.HTTP_400_BAD_REQUEST)

    
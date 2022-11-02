from urllib import request

from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from events.models import Event, Team, TeamMembers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class TeamSerializer(serializers.Serializer):
    event_id = serializers.UUIDField(required=True)
    team_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    id = serializers.UUIDField(required=False)

    def create(self, validated_data):
        # save to DB
        event_id = validated_data["event_id"]
        if "team_name" in validated_data:
            team_name = validated_data["team_name"]
        else:
            team_name = ""

        event = Event.objects.get(id=event_id)

        if event.min_team_size == 1:
            valid_team = True

        if team_name is None:
            team_name = ""

        return Team.objects.create(
            name=team_name, event=event, join_url="", is_registered=valid_team
        )

    def validate(self, attrs):
        # validate the data - event exists and team name is present if team event
        event_id = attrs["event_id"]
        user = self.context.get("user")

        if "team_name" in attrs:
            team_name = attrs["team_name"]
        else:
            team_name = None

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            event = None

        if event is None:
            raise NotFound("event not found")

        # print(user.id)
        # print(event.teamsregistered.filter(user=1))

        if event.type == "INDIVIDUAL":
            if team_name is not None:
                raise ValidationError(
                    {"error": "team_name should be absent for individual events"}
                )
        else:
            if team_name is None:
                raise ValidationError(
                    {"error": "team_name should be present for team events"}
                )

        if team_name is not None and len(team_name.strip()) == 0:
            raise ValidationError({"error": "team_name must not be blank"})
        return attrs


class TeamMembersSerializer(serializers.Serializer):
    team_id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)
    is_leader = serializers.BooleanField(required=False)

    def create(self, validated_data):
        # save to DB
        team_id = validated_data["team_id"]
        user_id = validated_data["user_id"]
        team = Team.objects.get(id=team_id)
        # user = User.objects.get(id = user_id)
        user = None
        user = self.context.get("user")
        # if request and hasattr(request, "user"):
        # user = request.user

        if TeamMembers.objects.filter(team=team).exists():
            is_leader = False
        else:
            is_leader = True

        return TeamMembers.objects.create(team=team, user=user, is_leader=is_leader)

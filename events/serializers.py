from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from events.models import Event, Team, TeamMembers


class EventSerializer(serializers.ModelSerializer):
    club_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    def get_club_name(self, obj):
        return obj.club.name


class TeamSerializer(serializers.Serializer):
    event_id = serializers.UUIDField(required=True)
    team_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    id = serializers.UUIDField(required=False)

    def create(self, validated_data):
        user = self.context.get("user")
        event_id = validated_data["event_id"]
        team_name = validated_data["team_name"]

        event = Event.objects.get(id=event_id)

        valid_team = False
        if event.min_team_size == 1:
            valid_team = True

        if team_name is None:
            team_name = ""

        team_obj = Team.objects.create(
            name=team_name, event=event, is_registered=valid_team
        )

        TeamMembers.objects.create(team=team_obj, user=user, is_leader=True)

        return team_obj

    def validate(self, attrs):
        # validate the data - event exists and team name is present if team event
        event_id = attrs.get("event_id")

        team_name = attrs.get("team_name")

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            event = None

        if event is None:
            raise NotFound("event not found")

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
        team_id = validated_data["team_id"]
        user_id = validated_data["user_id"]

        return TeamMembers.objects.create(
            team_id=team_id, user_id=user_id, is_leader=False
        )

    def validate(self, attrs):
        team_id = attrs.get("team_id")
        try:
            team = Team.objects.get(id=team_id)
        except Exception:
            raise NotFound("Team ID Invalid")

        if team.event.max_team_size == team.user.all().count():
            raise ValidationError({"error": "Team reached it's max size"})
        return super().validate(attrs)

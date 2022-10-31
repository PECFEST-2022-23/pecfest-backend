from rest_framework import serializers
from rest_framework.exceptions import NotFound

from events.models import Event, Team


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class TeamSerializer(serializers.Serializer):
    event_id = serializers.UUIDField(required=True)
    team_name = serializers.CharField(required=False)

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

    def validate_event_id(self, value):
        # check if event exists
        try:
            event = Event.objects.get(id=value)
        except Event.DoesNotExist:
            event = None

        if event is None:
            raise NotFound("event not found")
        return value

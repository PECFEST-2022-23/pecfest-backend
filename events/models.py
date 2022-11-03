import uuid

from authentication.models import User
from django.db import models

from events.constants import ClubTypes, EventSubTypes, EventTypes


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=15, choices=ClubTypes)


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=15, choices=EventTypes, default=EventTypes.individual
    )
    description = models.TextField()
    datetime = models.DateTimeField()
    duration = models.TimeField()
    venue = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    max_team_size = models.IntegerField(default=1)
    min_team_size = models.IntegerField(default=1)
    image_url = models.ImageField()
    subtype = models.CharField(
        max_length=15, choices=EventSubTypes, default=EventSubTypes.dance
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, null=True, blank=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="teamsregistered"
    )
    is_registered = models.BooleanField(default=False)


class TeamMembers(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    is_leader = models.BooleanField(default=False)

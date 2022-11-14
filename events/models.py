import uuid

from authentication.models import User
from django.db import models

from events.constants import CategorySubTypes, CategoryTypes, ClubTypes, EventTypes


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=15, choices=ClubTypes)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="club")

    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=15, choices=EventTypes, default=EventTypes.individual, editable=False
    )
    category = models.CharField(
        max_length=15, choices=CategoryTypes, default=CategoryTypes.technical
    )
    description = models.TextField()
    startdatetime = models.DateTimeField()
    enddatetime = models.DateTimeField()
    venue = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="events")
    max_team_size = models.IntegerField(default=1, editable=False)
    min_team_size = models.IntegerField(default=1, editable=False)
    image_url = models.ImageField()
    subcategory = models.CharField(
        max_length=15, choices=CategorySubTypes, default=CategorySubTypes.dance
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    rulebook_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25, null=True, blank=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="teamsregistered"
    )
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TeamMembers(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    is_leader = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "team",
            "user",
        )

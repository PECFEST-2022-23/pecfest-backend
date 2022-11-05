from django.contrib import admin
from events.models import Event, Club, Team, TeamMembers

admin.site.register(Event)
admin.site.register(Club)
admin.site.register(Team)
admin.site.register(TeamMembers)

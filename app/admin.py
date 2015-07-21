from django.contrib import admin

from .models import Player, Card, Team, History

admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Team)
admin.site.register(History)

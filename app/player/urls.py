from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<id>\w+)?$', "app.player.views.player", name="player data"),
    url(r'^feed/(?P<id>\w+)$', "app.player.views.feed", name="feed player")
]

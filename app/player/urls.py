from django.conf.urls import include, url

urlpatterns =[
    url(r'^(?P<id>\w+)$', "app.player.views.player", name="player data"),
    url(r'^edit/(?P<id>\w+)$', "app.player.views.edit", name="edit player data")
]

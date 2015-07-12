from django.conf.urls import include, url

urlpatterns =[
    url(r'^', "app.player.views.player", name="player data"),
]

from django.conf.urls import include, url

urlpatterns =[
    url(r'^', "app.player.views.player", name="player data"),
    url(r'^history', 'app.player.views.history', name="history"),
    url(r'^edit', "app.player.views.edit", name="edit player data")
]

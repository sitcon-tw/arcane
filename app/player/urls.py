from django.conf.urls import include, url

urlpatterns =[
    url(r'^player/', "app.player.views.player", name="edit player data"),
    url(r'^player/edit/', "app.player.views.edit", name="edit player data")
]

from django.conf.urls import include, url


urlpatterns = [
    url(r'^card/', "app.card.views.card", name="card"),
    url(r'^card/get/', "app.card.views.get", name="get"),
    url(r'^card/edit/', "app.card.views.edit", name="edit card")
]

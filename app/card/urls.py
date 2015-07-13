from django.conf.urls import include, url


urlpatterns = [
    url(r'^generate', "app.card.views.gen", name="generate card"),
    url(r'^get/', "app.card.views.get", name="get"),
    url(r'^edit/', "app.card.views.edit", name="edit card")
]

from django.conf.urls import url


urlpatterns = [
    url(r'^generate/$', "app.card.views.gen", name="generate card"),
    url(r'^get/(?P<id>\w{16})$', "app.card.views.get", name="get"),
    url(r'^edit/(?P<id>\w{16})$', "app.card.views.edit", name="edit card"),
    url(r'^(?P<id>\w{16})$', "app.card.views.card", name="view card"),
]

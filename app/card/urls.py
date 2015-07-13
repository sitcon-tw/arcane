from django.conf.urls import include, url


urlpatterns = [
    url(r'^\w{16}$', "app.card.views.card", name="view card"),
    url(r'^generate/\w{16}$', "app.card.views.gen", name="generate card"),
    url(r'^get/\w{16}$', "app.card.views.get", name="get"),
    url(r'^edit/\w{16}$', "app.card.views.edit", name="edit card")
]

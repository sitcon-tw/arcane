from django.conf.urls import url

urlpatterns = [
    url(r'^$', "app.staff.views.dashboard", name="dashboard"),
    url(r'^gift$', "app.staff.views.gift", name="fast send"),
]

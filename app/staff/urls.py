from django.conf.urls import url

urlpatterns = [
    url(r'^', "app.staff.views.dashboard", name="dashboard"),
]

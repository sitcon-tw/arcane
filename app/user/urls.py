from django.conf.urls import include, url

urlpatterns =[
    url(r'^chgpin', "app.user.views.chgpin", name="change user pin"),
    url(r'^chgname', "app.user.views.chgname", name="change user name"),
    url(r'^login', "app.user.views.logout", name="login"),
    url(r'^logout', "app.user.views.logout", name="logout")
]

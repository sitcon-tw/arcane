from django.conf.urls import include, url

urlpatterns =[
    url(r'^chgpin', "app.user.views.chgpin", name="change user pin"),
    url(r'^chgname', "app.user.views.chgname", name="change user name"),
    url(r'^login', "app.user.views.login", name="login"),
    url(r'^staff_login', "app.user.views.staff_login", name="staff login"),
    url(r'^logout', "app.user.views.logout", name="logout")
]

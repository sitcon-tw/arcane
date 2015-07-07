from django.conf.urls import include, url

urlpatterns =[
    url(r'^user/chgpin', "app.user.views.chgpin", name="change user pin"),
    url(r'^user/chgname', "app.user.views.chgname", name="change user name"),
    url(r'^user/login', "app.user.views.logout", name="login"),
    url(r'^user/logout', "app.user.views.logout", name="logout")
]

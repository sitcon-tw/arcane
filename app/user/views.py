from django.contrib.auth import views as auth_view
from django.shortcuts import render, redirect


def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    return auth_view.login(request, template_name='user/login.html')


def logout(request):
    return auth_view.logout_then_login(request, 'login')


def chgpin(request):
    pass

def chgname(request):
    pass

def staff_login(request):
    pass

from django.contrib.auth import views as auth_view
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_function
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from app.user.forms import LoginForm


def login(request, id=None):
    if request.user.is_authenticated():
        return redirect('home')
    if not request.POST:
        form = LoginForm()
        return render(request, "user/login.html", locals())
    else:
        username = id
        password = request.POST.get("password", '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login_function(request, user)
                return redirect('home')
            else:
                error = "奇怪的錯誤"
                return render(request, "user/login.html", locals())
        else:
            error = "錯誤的PIN碼"
            return render(request, "user/login.html", locals())


def logout(request):
    return auth_view.logout_then_login(request, 'home')


@login_required
def chgpin(request):
    if not request.user.is_authenticated():
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'user/chgpin.html', {"form": PasswordChangeForm()})


def chgname(request):
    pass


def staff_login(request):
    if request.user.is_authenticated():
        return redirect('home')
    return auth_view.login(request, template_name='user/staff_login.html')

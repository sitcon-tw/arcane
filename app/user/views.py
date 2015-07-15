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
    else:
        try:
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)

    if not request.POST:
        form = LoginForm
        return render(request, "user/login.html", locals())
    else:
        username = id
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=user.username, password=form.cleaned_data["password"])
            if user is not None:
                if user.is_active:
                    login_function(request, user)
                    return redirect('home')
                else:
                    return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)
            else:
                return redirect('login', id)
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

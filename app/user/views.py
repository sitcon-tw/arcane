from app.user.forms import LoginForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import views as auth_view
from django.contrib.auth import authenticate
from django.contrib.auth.views import password_change
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from app.user.forms import PasswordChangeForm, ChangeNameForm
# from app.user.forms import PasswordChangeForm


def login(request, id=None):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        if not User.objects.filter(username=id).exists():
            return render(
                request, "submit.html", {
                    "content": ("<h1>Wrong user</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; url=/\">"),
                    "title": "錯誤！"}, status=404)

    if not request.POST:
        form = LoginForm()
        return render(request, "user/login.html", locals())
    else:
        username = id
        password = request.POST.get("password", '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('home')
            else:
                error = "奇怪的錯誤"
                return render(request, "user/login.html", locals())
        else:
            error = "錯誤的PIN碼"
            return render(request, "user/login.html", locals())


def logout(request):
    return auth_view.logout_then_login(request, 'home')


def chgpin(request):
    if not request.user.is_authenticated():
        return redirect('home')
    return password_change(request, template_name='user/chgpin.html',
                           post_change_redirect='home', password_change_form=PasswordChangeForm)


def chgname(request):
    if not request.user.is_authenticated():
        return redirect('home')
    message = ""
    if not request.method == 'GET':
        form = ChangeNameForm({
            "first_name": request.POST.get('first_name', ''),
            "last_name": request.POST.get('last_name', ''),
        })
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
        return redirect('home')

    form = ChangeNameForm({
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    })
    return render(request, 'user/chgname.html', {"form": form, "message": message})


def staff_login(request):
    if request.user.is_authenticated():
        return redirect('home')
    return auth_view.login(request, template_name='user/staff_login.html')

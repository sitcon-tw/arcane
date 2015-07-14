from django.shortcuts import render, redirect

def home(request):
    if not request.user.is_authencated:
        return render(request, "submit.html", {"content": "<h1>SITCON 夏令營點數系統</h1>", "title":"首頁"})
    else:


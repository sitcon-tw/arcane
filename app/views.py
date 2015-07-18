from app.models import is_player
from django.shortcuts import redirect, render


def home(request):
    if not request.user.is_authenticated():
        return render(request, "submit.html", {"content": "<h1>SITCON 夏令營點數系統</h1>", "title":"首頁"})
    elif is_player(request.user):
        return redirect("player data")
    else:
        return redirect("dashboard")

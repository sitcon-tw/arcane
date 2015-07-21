from app.models import is_player
from django.shortcuts import redirect, render


def home(request):
    if not request.user.is_authenticated():
        return render(request, "index.html")
    elif is_player(request.user):
        return redirect("player data")
    else:
        return redirect("dashboard")

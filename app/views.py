from django.shortcuts import redirect, render


def home(request):
    if not request.user.is_authenticated():
        return render(request, "index.html")
    elif request.user.is_staff:
        return redirect("dashboard")
    else:
        return redirect("player data")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import Player, is_player

def player(request, id=None):
    if not request.user.is_authenticated():
        try:
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)

        return redirect("/user/login/" + id)
    else:
        if request.user.is_staff:
            try:
                user = User.objects.get(username=id)
            except ObjectDoesNotExist:
                return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)

            player = user.player
            return render(request, 'player/player.html', locals())
        elif is_player(request.user):
            user = request.user
            return render(request, 'player/player.html', locals())

def edit(request):
    pass

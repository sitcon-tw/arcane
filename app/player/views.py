from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import is_player

@login_required(login_url="/user/login")
def player(request):
    if not is_player(request.user):
        raise PermissionDenied
    else:
        user = request.user
        player = request.user.player
        return render(request, 'player/player.html', locals())

def edit(request):
    pass

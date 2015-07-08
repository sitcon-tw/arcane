from django.shortcuts import render

def player(request):
    return render(request, 'player/player.html', locals())

def edit(request):
    pass

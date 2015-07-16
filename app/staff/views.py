from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app import models as data


@login_required
def dashboard(request):
    players = data.Player.objects.all()
    cards = data.Card.objects.all()
    teams = data.Team.objects.all()
    historys = data.History.objects.all()
    return render(request, 'staff/dashboard.html', locals())

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from djanog.core.exceptions import PermissionDenied

from app import models as data
from app.staff.forms import FastSendForm
from app.models import Card, History


@login_required
def dashboard(request):
    if not request.is_staff:
        raise PermissionDenied
    players = data.Player.objects.all()
    cards = data.Card.objects.all()
    teams = data.Team.objects.all()
    history_entries = data.History.objects.all()
    return render(request, 'staff/dashboard.html', locals())


@login_required
def gift(request):
    if request.method == 'GET':
        return render(request, 'staff/gift.html', {"form": FastSendForm()})
    else:
        form = FastSendForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['player']
            card = Card()
            card.name = "來自 %s 的祝福" % request.user.get_full_name()
            card.value = form.cleaned_data['point']
            card.comment = form.cleaned_data['message']
            card.active = True
            card.retrieved = True
            card.issuer = request.user
            card.capturer = player
            card.save()
            record_reciever = History(
                action=0xfeed, user=player.user, card=card,
                comment="從 %s 收到一張卡片" % request.user.get_full_name())
            record_reciever.save()
            record_sender = History(
                action=0xfeed, user=request.user, card=card,
                comment="給了 %s (%s)" % (player.user.get_full_name(), player.user.username))
            record_sender.save()
            return render(
                request, "submit.html", {
                    "success": True,
                    "title": "成功發送卡片",
                    "content": "成功將卡片送給 %s 了！" % player.user.get_full_name(),
                })
        else:
            return render(
                request, "submit.html", {
                    "success": False,
                    "title": "發送卡片失敗",
                    "content": "要不要去戳戳系統管理員呢？"
                })

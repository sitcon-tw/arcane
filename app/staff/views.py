from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.db import transaction, models

from app import models as data
from app.staff.forms import FastSendForm
from app.models import Card, History, user_permission


@login_required
def dashboard(request):
    if user_permission(request.user) < 2:
        raise PermissionDenied
    if user_permission(request.user) < 3:
        return redirect('lite')
    players = data.Player.objects.all()
    cards = data.Card.objects.all()
    teams = data.Team.objects.all()
    history_entries = data.History.objects.all().order_by('-date')[:30]
    return render(request, 'staff/dashboard.html', locals())

@login_required
def leaderboard(request):
    if user_permission(request.user) < 2:
        raise PermissionDenied
    if user_permission(request.user) < 3:
        return redirect('lite')
    players = data.Player.objects.all()
    cards = data.Card.objects.all()
    lencards = len(cards)
    lencardsgot = len([x for x in cards if x.retrieved])
    totalpoints = data.Card.objects.filter(active=True).aggregate(models.Sum('value'))["value__sum"]
    totalpointsgot = data.Card.objects.filter(retrieved=True).aggregate(models.Sum('value'))["value__sum"]
    teams = data.Team.objects.all().exclude(tid="zsh")
    sorted_teams = list(teams)
    sorted_teams.sort(key=lambda x: x.points, reverse=True)
    history_entries = data.History.objects.all().order_by('-date')[:30]
    return render(request, 'staff/leaderboard.html', locals())


@login_required
def lite(request, tt=None):
    denomination = [64, 128, 256, -64]
    if user_permission(request.user) < 2:
        raise PermissionDenied
    if tt is not None:
        try:
            tt = int(tt)
        except:
            return render(
                request, "submit.html", {
                    "success": False,
                    "title": "發送卡片失敗",
                    "content": "我幫你綁好繩子了，"
                    "你要自己跳還是我推你跳呢？（本繩載重20g）"})
        if tt not in range(0, len(denomination)):
            return render(
                request, "submit.html", {
                    "success": False,
                    "title": "發送卡片失敗",
                    "content": "要不要去戳戳系統管理員呢？"
                    "(如果是POST奇怪的資料，可能會收到彈力繩喔ˊ_>ˋ)"
                })
        with transaction.atomic():
            card = Card()
            present = request.user.first_name
            if present == "":
                present = '祝福'
            card.name = "來自 %s 的%s" % (request.user.last_name, present)
            card.value = denomination[tt]
            card.active = True
            card.retrieved = False
            card.issuer = request.user
            card.save()
            record = History(action=1, user=request.user, card=card)
            record.save()
        return redirect('view card', card.cid)
    else:
        return render(request, 'staff/lite.html',locals())


@login_required
def gift(request):
    if user_permission(request.user) < 3:
        raise PermissionDenied
    if request.method == 'GET':
        return render(request, 'staff/gift.html', {"form": FastSendForm()})
    else:
        form = FastSendForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['player']
            card = Card()
            # hard code
            present = request.user.first_name
            if present == "":
                present = '祝福'
            with transaction.atomic():
                card.name = "來自 %s 的%s" % (request.user.last_name, present)
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
                    "(如果是POST奇怪的資料，可能會收到彈力繩喔ˊ_>ˋ)"
                })

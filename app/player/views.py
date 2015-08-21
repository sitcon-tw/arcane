from app.models import History
from app.player.forms import FeedForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.db import transaction


def player(request, id=None):
    if not request.user.is_authenticated():
        return redirect("login", id)
    else:
        if request.user.is_staff:
            return redirect('home')
        if not id == request.user.username:
            # rediect logged-in user to /player/<username>
            return redirect('player data', request.user.username)
        else:
            user = request.user
            sorted_players = list(user.player.team.player.all())
            sorted_players.sort(key=lambda x: x.points_acquired, reverse=True)
            this_records = History.objects.filter(user=user)
            fun = True
            records = []
            for player_i in user.player.team.player.all():
                records = records + list(History.objects.filter(user=player_i.user))
            for i in sorted_players:
                if user.player.team.points == 0:
                    i.weight = 0
                else:
                    i.weight = i.points_acquired / user.player.team.points * 100
            return render(request, 'player/player.html', locals())


@login_required
def feed(request, id=None):
    if request.user.has_perm('app.feed_card'):
        try:
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            return render(
                request, "submit.html", {
                    "content": "你是找誰？",
                    "title": "錯誤！"}, status=404)

        else:
            if not request.POST:
                form = FeedForm()
                return render(request, "player/feed.html", locals())
            else:
                form = FeedForm(request.POST)
                if form.is_valid():
                    with transaction.atomic():
                        player = user.player
                        card = form.cleaned_data["card"]
                        card.capturer = player
                        card.retrieved = True
                        card.save()
                        record_sender = History(
                            action=0xfeed, user=request.user, card=card,
                            comment="給了 %s (%s)" % (player.user.get_full_name(), player.user.username))
                        record_sender.save()
                        record_reciever = History(
                            action=0xfeed, user=player.user, card=card,
                            comment="從 %s 收到一張卡片" % request.user.get_full_name())
                        record_reciever.save()

                    return render(
                        request, "submit.html", {
                            "title": "成功發送",
                            "content": "你送給 %s 一張卡片" % player.user.get_full_name(),
                        })
                else:
                    return render(request, "player/feed.html", locals())
    else:
        return render(
            request, "submit.html", {
                "content": "工作人員的世界你是看不到的!",
                "title": "錯誤！"}, status=403)

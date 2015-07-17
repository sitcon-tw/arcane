from app.models import Card, History, is_player
from app.player.forms import FeedForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import redirect, render


def player(request, id=None):
    if not request.user.is_authenticated():
        if not User.objects.filter(username=id).exists():
            return render(
                request, "submit.html", {
                    "content": ("<h1>Wrong user</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; url=/\">"),
                    "title": "錯誤！"}, status=404)
        return redirect("login", id)
    else:
        if not id == request.user.username:
            # rediect logged-in user to /player/<username>
            return redirect('player data', request.user.username)
        if not is_player(request.user):
            # ban non player
            raise PermissionDenied
        else:
            user = request.user
            records = History.objects.filter(user=user)
            return render(request, 'player/player.html',
                          {"user": user, "records": records})

@login_required
def feed(request, id=None):
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        try:
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            return render(
                request, "submit.html", {
                    "content":("<h1>Wrong user</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; url=/\">"),
                    "title":"錯誤！"}, status=404)

        if not is_player(user):
            return render(
                request, "submit.html", {
                    "content":("<h1>Wrong user</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; url=/\">"),
                    "title":"錯誤！"}, status=404)
        else:
            if not request.POST:
                form = FeedForm()
                return render(request, "player/feed.html", locals())
            else:
                form = FeedForm(request.POST)
                if form.is_valid():
                    player = user.player
                    card = form.cleaned_data["card"]
                    player.captured_card.add(card)
                    player.save()
                    card.retrieved = True
                    card.save()
                    record = History(action=0xfeed, user=request.user, card=card,
                                     comment="給" + user.get_full_name + " (" + user.username + ")")
                    record.save()
                    card.save()

                    return render(
                        request, "submit.html", {
                            "content":("<h1>Submitted.</h1>"
                                       "<meta http-equiv=\"refresh\" content=\"3; "
                                       "url=\"/\">")})
                else:
                    return render(request, "player/feed.html", locals())

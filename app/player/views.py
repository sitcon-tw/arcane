from app.models import Player, is_player, Card, History
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import redirect, render


def player(request, id=None):
    if not request.user.is_authenticated():
        return redirect("login", id)
    else:
        if not id == request.user.username:
# rediect logged-in user to /player/<username>
            return redirect('player data', request.user.username)
        if request.user.is_staff:
# ban staff
            raise PermissionDenied
        else:
            user = request.user
            records = History.objects.filter(user=user)
            return render(request, 'player/player.html',
                          {"user": user, "records": records})


def edit(request, id=None):
    pass
"""
# Edit Player Function, will implement if requested
@login_required
def edit(request, id=None):
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
                form = PlayerForm({
                    "name": user.username})
                return render(request, "card/edit.html", locals())
            else:
                form = CardForm(request.POST)
                if form.is_valid():
                    card = Card()
                    card.name = form.cleaned_data["name"]
                    card.value = form.cleaned_data["value"]
                    card.long_desc = form.cleaned_data["long_desc"]
                    card.active = form.cleaned_data["active"]
                    card.save()
                return render(
                    request, "submit.html", {
                        "content":("<h1>Submitted.</h1>"
                                   "<meta http-equiv=\"refresh\" content=\"3; "
                                   "url=/card/" + card.cid + "\">")})
"""

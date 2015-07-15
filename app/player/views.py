from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.models import User
from app.models import Player, is_player, Card


def player(request, id=None):
    if not request.user.is_authenticated():
        if not User.objects.filter(username=id).exists():
            return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)
        return redirect("login", id)
    else:
        if not id:
# rediect logged-in user to /player/<username>
            return redirect('player data', request.user.username)
        if request.user.is_staff:
# ban staff
            raise PermissionDenied
        else:
            user = request.user
            return render(request, 'player/player.html', {"user": user})


@login_required
def edit(request, id=None):
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        try:
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)
        if not is_player(user):
            return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)
        else:
            if not request.POST:
                form = PlayerForm({"name": user.username, "value": card.value, "long_desc": card.long_desc, "active": card.active, "retrieved": card.retrieved, "modified_reason": ""})
                return render(request, "card/edit.html", locals())
            else:
                form = CardForm(request.POST)
                if form.is_valid():
                    card = Card()
                    card.name = form.cleaned_data["name"]
                    card.value = form.cleaned_data["value"]
                    card.long_desc = form.cleaned_data["long_desc"]
                    card.active = form.cleaned_data["active"]
                    card.modified_reason = form.cleaned_data["modified_reason"]
                    card.save()
                return render(request, "submit.html", {"content": "<h1>Submitted.</h1><meta http-equiv=\"refresh\" content=\"3; url=/card/" + card.cid + "\">"})

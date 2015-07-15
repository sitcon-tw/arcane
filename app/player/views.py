from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
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
        no_id = False
        try:
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            no_id = True

        if request.user.is_staff and not no_id:
            player = user.player
            return render(request, 'player/player.html', locals())
        elif is_player(request.user):
            user = request.user
            return render(request, 'player/player.html', locals())
        else:
            return render(request, "submit.html", {"content":"<h1>Wrong user</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">", "title":"錯誤！"}, status=404)

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
                    card.name = form.cleaned_data["name"]
                    card.value = form.cleaned_data["value"]
                    card.long_desc = form.cleaned_data["long_desc"]
                    card.active = form.cleaned_data["active"]
                    card.modified_reason = form.cleaned_data["modified_reason"]
                    card.save()
                return render(request, "submit.html", {"content": "<h1>Submitted.</h1><meta http-equiv=\"refresh\" content=\"3; url=/card/" + card.cid + "\">"})

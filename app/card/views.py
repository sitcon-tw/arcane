from app.card.forms import CardForm
from app.models import Card, History, is_player
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render


@login_required
def card(request, id=None):
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        try:
            card = Card.objects.get(cid=id)
        except ObjectDoesNotExist:
            return render(
                request, "submit.html", {
                    "content":("<h1>Wrong card</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; url=/\">"),
                    "title":"錯誤！"}, status=404)
        retriever = card.capturer
        host = request.META['HTTP_HOST']
        return render(request, "card/card.html", locals())


@login_required
def edit(request, id=None):
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        try:
            card = Card.objects.get(cid=id)
        except ObjectDoesNotExist:
            return render(
                request, "submit.html", {
                    "content":("<h1>Wrong card</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; url=/\">"),
                    "title":"錯誤！"}, status=404)

        if not request.POST:
            form = CardForm(
                {"name": card.name,
                 "value": card.value,
                 "long_desc": card.long_desc,
                 "active": card.active,
                 "retrieved": card.retrieved})
            return render(request, "card/edit.html", locals())
        else:
            form = CardForm(request.POST)
            if form.is_valid():
                action = 2
                if card.active is not form.cleaned_data["active"]:
                    if form.cleaned_data["active"]:
                        action = 4
                    else:
                        action = 3
                card.name = form.cleaned_data["name"]
                card.value = form.cleaned_data["value"]
                card.long_desc = form.cleaned_data["long_desc"]
                card.active = form.cleaned_data["active"]
                card.save()
                record = History(action=action, user=request.user, card=card)
                record.save()
            return render(
                request, "submit.html", {
                    "content": ("<h1>Submitted.</h1>"
                                "<meta http-equiv=\"refresh\" content=\"3; "
                                "url=/card/" + card.cid + "\">")})


def get(request, id=None):
    if not is_player(request.user):
        return render(
            request, "submit.html", {
                "content":("<h1>你沒有登入！</h1>"
                           "你可能需要先掃描一下識別證上的 QR_Code 來登入系統"),
                "title":"未登入！"}, status=404)
    else:
        try:
            card = Card.objects.get(cid=id)
        except ObjectDoesNotExist:
            return render(
                request, "submit.html", {
                    "content":("<h1>Wrong card</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; url=/\">"),
                    "title":"錯誤！"}, status=404)

        if not request.method == 'POST':
            form = CardForm({
                "name": card.name,
                "value": card.value,
                "long_desc": card.long_desc,
                "active": card.active,
                "retrieved": card.retrieved})
            return render(request, "card/get.html", locals())
        else:
            if is_player(request.user):
                # Add points
                player = request.user.player
                player.captured_card.add(card)
                player.save()
                card.retrieved = True
                card.save()
                record = History(action=10, user=request.user, card=card)
                record.save()

                return render(
                    request, "submit.html", {
                        "content": ("<h1>Submitted.</h1>"
                                   "<meta http-equiv=\"refresh\" content=\"3; url=\"/\">")})
            else:
                raise PermissionDenied


@login_required
def gen(request):
    if request.user.is_staff:
        if not request.POST:
            form = CardForm()
            return render(request, "card/generate.html", locals())
        else:
            form = CardForm(request.POST)
            if form.is_valid():
                card = Card()
                card.name = form.cleaned_data["name"]
                card.value = form.cleaned_data["value"]
                card.long_desc = form.cleaned_data["long_desc"]
                card.active = form.cleaned_data["active"]
                card.issuer = request.user
                card.save()
                record = History(action=1, user=request.user, card=card)
                record.save()
            return render(
                request, "submit.html", {
                    "content":("<h1>Submitted.</h1>"
                               "<meta http-equiv=\"refresh\" content=\"3; "
                               "url=/card/" + card.cid + "\">")})
    else:
        raise PermissionDenied

@login_required
def feed(request, id=None):
    pass

from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse
from app.models import Card
from app.card.forms import CardForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied


def card(request, id=None):
    try:
        card = Card.objects.get(cid=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("<h1>Wrong card</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">")
    get_url = "http://" + request.META['HTTP_HOST'] + "/card/get/" + card.cid
    return render(request, "card/card.html", locals())


def edit(request, id=None):
    if not request.user.is_staff:
        raise PermissionDenied
    try:
        card = Card.objects.get(cid=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("<h1>Wrong card</h1><meta http-equiv=\"refresh\" content=\"3; url=/\">")

    if not request.POST:
        form = CardForm({"name": card.name, "value": card.value, "long_desc": card.long_desc, "active": card.active, "retrieved": card.retrieved, "modified_reason": ""})
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
        return HttpResponse("<h1>Submitted.</h1><meta http-equiv=\"refresh\" content=\"3; url=/card/" + card.cid + "\">")


def get(request, id=None):
    pass


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
                card.modified_reason = form.cleaned_data["modified_reason"]
                card.save()
            return HttpResponse("<h1>Submitted.</h1><meta http-equiv=\"refresh\" content=\"3; url=/card/" + card.cid + "\">")
    else:
        raise PermissionDenied

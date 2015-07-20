from app.card.forms import CardForm, FeedForm
from app.models import Card, History, is_player
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db import transaction


def CardNotFound(request):
    return render(
        request, "submit.html", {
            "success": False,
            "content": "不在系統中的卡片，可能是被註銷了，請戳戳工作人員吧",
            "title": "不認識的卡片"}, status=404)


@login_required
def card(request, id=None):
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        try:
            card = Card.objects.get(cid=id)
        except ObjectDoesNotExist:
            return CardNotFound(request)
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
            return CardNotFound(request)
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
                with transaction.atomic():
                    card.name = form.cleaned_data["name"]
                    card.value = form.cleaned_data["value"]
                    card.long_desc = form.cleaned_data["long_desc"]
                    card.active = form.cleaned_data["active"]
                    card.save()
                    record = History(action=action, user=request.user, card=card)
                    record.save()
            else:
                return render(
                    request, "submit.html", {
                        "success": True,
                        "title": "編輯失敗",
                        "next_page": reverse('home'),
                    })
            return render(
                request, "submit.html", {
                    "success": True,
                    "title": "成功編輯",
                    "content": "成功編輯卡片 %s" % card.name,
                    "next_page": reverse('view card', args=[card.cid]),
                })


def get(request, id=None):
    if not is_player(request.user):
        return render(
            request, "submit.html", {
                "success": False,
                "content": "你可能需要先掃描一下識別證上的 QR_Code 來登入系統",
                "title": "未登入！"}, status=404)
    else:
        try:
            card = Card.objects.get(cid=id)
        except ObjectDoesNotExist:
            return CardNotFound(request)

        if is_player(request.user):
            if not card.retrieved and card.active:
                # Add points
                with transaction.atomic():
                    player = request.user.player
                    player.captured_card.add(card)
                    player.save()
                    card.retrieved = True
                    card.save()
                    record = History(action=10, user=request.user, card=card)
                    record.save()
                abscardvalue = abs(card.value)
                return render(
                    request, "card/get.html", locals())
            else:
                return render(
                    request, "submit.html", {
                        "success": False,
                        "title": "卡片已被捕獲",
                        "content": "這張卡片已經被使用過囉，何不換張卡片呢？",
                    })
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
                with transaction.atomic():
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
                        "success": True,
                        "title": "一張卡片就此誕生！",
                        "content": "生成了一張卡片 %s 含有 %d 點" % (card.name, card.value),
                        "next_page": reverse('view card', args=[card.cid]),
                    })
            else:
                return render(request, "submit.html", {
                    "success": False,
                    "title": "產生卡片失敗",
                    "content": "要不要去戳戳系統管理員呢？"
                    "(如果是POST奇怪的資料，可能會收到彈力繩喔ˊ_>ˋ)"
                    })
    else:
        raise PermissionDenied


@login_required
def feed(request, id=None):
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        try:
            card = Card.objects.get(cid=id)
        except ObjectDoesNotExist:
            return CardNotFound(request)

        if not card.active or card.retrieved:
            return render(
                request, "submit.html", {
                    "success": False,
                    "title": "卡片已被捕獲",
                    "content": "這張卡片已經被使用過囉，何不換張卡片呢？",
                })
        else:
            if not request.POST:
                form = FeedForm()
                return render(request, "card/feed.html", locals())
            else:
                form = FeedForm(request.POST)
                if form.is_valid():
                    with transaction.atomic():
                        player = form.cleaned_data["player"]
                        card.retrieved = True
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

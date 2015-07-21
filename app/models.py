from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string


class Team(models.Model):
    tid = models.CharField(max_length=32,
                           primary_key=True,
                           verbose_name="Team ID",
                           help_text="Alphanumeric name for the team.")
    name = models.CharField(max_length=100,
                            verbose_name="Name",
                            help_text="Name of the team.")

    @property
    def points(self):
        s = 0
        for player in self.player.all():
            s += player.points_acquired
        return s

    def __str__(self):
        return str(self.name) + " (" + str(self.tid) + ")"


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, verbose_name="User", help_text="The user of this player.")
    team = models.ForeignKey(Team,
                             verbose_name="Team",
                             help_text="The team this player belongs to.",
                             related_name="player")

    @property
    def points_acquired(self):
        s = self.captured_card.filter(active=True).aggregate(models.Sum('value'))
        if s['value__sum'] is None:
            return 0
        return s['value__sum']

    def __str__(self):
        return (str(self.user.get_full_name()) + " (" +
                str(self.user.get_username()) + "), " + self.team.name)


class Card(models.Model):
    def random():
        return str(get_random_string(16))
    cid = models.CharField(max_length=16,
                           primary_key=True,
                           default=random,
                           verbose_name="Card ID",
                           help_text="The unique ID for the points card.")
    value = models.IntegerField(default="1",
                                verbose_name="Value",
                                help_text="The value of the points card.")
    active = models.BooleanField(default=True, verbose_name="Active?")
    retrieved = models.BooleanField(default=False, verbose_name="Retrieved")
    name = models.CharField(
        max_length=32,
        verbose_name="Name",
        help_text="Name of the card.",
        blank=True)
    long_desc = models.TextField(verbose_name="Descriptions",
                                 help_text="Long descriptions about the card.",
                                 blank=True)
    issuer = models.ForeignKey(User, related_name="issued_card")
    capturer = models.ForeignKey(Player, related_name="captured_card", null=True, blank=True)

    def __str__(self):
        if self.active and not self.retrieved:
            return (str(self.name) + " (" + str(self.cid) + "), "
                    "active, " + str(self.value) + " points.")
        elif not self.active and self.retrieved:
            return (str(self.name) + " (" + str(self.cid) + "), "
                    "retrieved by " + str(self.capturer) + ", " + str(self.value) + " points.")
        else:
            return (str(self.name) + " (" + str(self.cid) + "), "
                    "inactive, " + str(self.value) + " points.")


class History(models.Model):
    ACTION_CODE = {
        1: "建立卡片",
        2: "編輯卡片",
        3: "關閉卡片",
        4: "啟動卡片",
        10: "獲得卡片",
        0xfeed: "餵食卡片",
    }

    no = models.AutoField(primary_key=True)
    action = models.IntegerField(choices=list(ACTION_CODE.items()))
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def action_explain(self):
        return History.ACTION_CODE[self.action]


def is_player(user):
    try:
        if user.player:
            return True
    except:
        return False


def user_permission(user):
    if not user.is_authenticated():
        return 0
    if is_player(user):
        return 1
    if user.groups.filter(name="worker").exists():
        return 2
    else:
        return 3

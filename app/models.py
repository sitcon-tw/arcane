from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class team(models.Model):
    tid = models.CharField(max_length=32, validators=[alphanumeric], primary_key=True)
    name = models.CharField(max_length=32, null=True)
    points = models.IntegerField(name="Points", verbose_name="The current amount of points of this group.", default=0)
    history = HistoricalRecords()

    def __str__(self):
        return self.name + ", currently has " + self.points + " points."


class player(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(team)
    points_acquired = models.IntegerField(name="Acquired Points", verbose_name="The amount of points acquired by this player.", default=0)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.get_full_name() + " (" + self.user.get_username() + "), acquired " + self.points_acquired + " points for " + self.team.name + ", which currently has " + self.team.points + " points."

class card(models.Model):
    cid = models.CharField(max_length=16, primary_key=True, default=get_random_string(16))
    value = models.IntegerField("The value of the points card.", "value", default="1")
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        if self.active:
            return "An active points card with " + self.value + " points, with the cid: \"" + self.cid + "\" ."
        else:
            return "An inactive points card with " + self.value + " points, with the cid: \"" + self.cid + "\" ."

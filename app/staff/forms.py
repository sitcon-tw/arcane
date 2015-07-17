from django import forms

from app.models import Player


class FastSendForm(forms.Form):
    message = forms.CharField(max_length=255, label="訊息", help_text="悄悄話", required=False)
    point = forms.IntegerField(label="價值", help_text="點數卡的價值", initial=1)
    player = forms.ModelChoiceField(Player.objects.all(), label="玩家")

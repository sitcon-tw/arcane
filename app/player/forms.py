from django import forms
from app.models import Card


class CardCoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s: %d point" % (obj.name, obj.value)


class FeedForm(forms.Form):
    card = CardCoiceField(Card.objects.filter(active=True, retrieved=False), label="Card")

from django import forms
from app.models import Card

class FeedForm(forms.Form):
    card = forms.ModelChoiceField(Card.objects.filter(active=True, retrieved=False), label="Card")

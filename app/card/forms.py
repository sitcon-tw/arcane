from django import forms

class CardForm(forms.Form):
    name = forms.CharField(max_length=32, label="名字", help_text="點數卡的名子")
    value = forms.IntegerField(label="值", help_text="點數卡的數值", initial="5")
    long_desc = forms.CharField(max_length=200, widget=forms.Textarea(), label="說明")

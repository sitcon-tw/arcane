from django import forms

class CardForm(forms.Form):
    name = forms.CharField(max_length=32, label="名字", help_text="點數卡的名子", required=False)
    value = forms.IntegerField(label="值", help_text="點數卡的數值", initial="5")
    long_desc = forms.CharField(max_length=200, widget=forms.Textarea(), label="說明", required=False)
    active = forms.BooleanField(label="開通", help_text="該點數卡是否可用", required=False)
    retrieved = forms.BooleanField(label="提領", help_text="該點數卡是否被提領了", required=False)
    modified_reason = forms.CharField(max_length=200, widget=forms.Textarea(), label="更動原因", required=False)

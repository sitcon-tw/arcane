from django import forms
from django.contrib.auth.forms import PasswordChangeForm as auth_pwchg_form


class LoginForm(forms.Form):
    password = forms.CharField(
        label="勇者密碼",
        widget=forms.PasswordInput(),
        help_text="應該會在識別證的前後左右 :)")


class ChangeNameForm(forms.Form):
    first_name = forms.CharField(label="姓", max_length=10)
    last_name = forms.CharField(label="名字", max_length=10)


PasswordChangeForm = auth_pwchg_form
PasswordChangeForm.error_messages['password_incorrect'] = "你的舊密碼不太對喔"
PasswordChangeForm.error_messages['password_mismatch'] = "你的確定打了兩次一樣的新密碼嗎？要不要再試試看？"

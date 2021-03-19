from django import forms

from my_auth.forms.login import MyLoginForm


class MyRegisterForm(MyLoginForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        fields = ('email', 'password', 'first_name', 'last_name')

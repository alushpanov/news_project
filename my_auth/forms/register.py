from django import forms
from django.core.exceptions import ValidationError

from my_auth.forms.login import MyLoginForm
from my_auth.models import MyUser


class MyRegisterForm(MyLoginForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        fields = ('email', 'password', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError('User with such email is already registered!')
        return email

from django import forms
from my_auth.models import MyUser


class MyLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'email'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'password'
        }
    ))

    class Meta:
        model = MyUser
        fields = ('email', 'password')

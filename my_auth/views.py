from django.contrib.auth import login as django_login, logout as django_logout
from django.shortcuts import redirect, render

from rest_framework.authtoken.views import ObtainAuthToken

from my_auth.api.serializers import UserSerializer
from my_auth.forms.login import LoginForm
from my_auth.forms.register import RegisterForm
from my_auth.models import MyUser


class LoginAuthToken(ObtainAuthToken):
    serializer_class = UserSerializer

    def get(self, request):
        return render(request, 'my_auth/login.html', {'form': LoginForm()})


def logout(request):
    django_logout(request)
    return redirect('my_auth:login')


def register(request):
    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if MyUser.objects.filter(email=email).exists():
                return render(request, 'my_auth/register.html', {
                    'form': form,
                    'msg': 'User with such email is already registered!'
                })
            else:
                user = MyUser.objects.create_user(**form.cleaned_data)
                django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('news:index')
    else:
        return render(request, 'my_auth/register.html', {'form': form})

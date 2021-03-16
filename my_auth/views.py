from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from my_auth.forms import MyLoginForm
from my_auth.models import MyUser


def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {})
    else:
        return redirect('my_auth:login')


def my_login(request):
    form = MyLoginForm()
    if request.POST:
        form = MyLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('my_auth:index')
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'msg': 'Login failed! Try again'
                })
    else:
        return render(request, 'login.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('my_auth:login')


def register(request):
    form = MyLoginForm()
    if request.POST:
        form = MyLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            if MyUser.objects.filter(email=email).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'msg': 'User with such email is already registered!'
                })
            else:
                user = MyUser.objects.create_user(email=email, password=password)
                user.save()
                login(request, user)
                return redirect('my_auth:index')
    else:
        return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from my_auth.forms import MyLoginForm
from my_auth.models import MyUser


def index_view(request):
    return render(request, 'index.html', {})


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
    return redirect('my_auth:index')


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

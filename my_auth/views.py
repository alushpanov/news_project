from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from my_auth.forms.login import MyLoginForm
from my_auth.forms.register import MyRegisterForm
from my_auth.models import MyUser


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
                return redirect('news:index')
            else:
                return render(request, 'my_auth/login.html', {
                    'form': form,
                    'msg': 'Login failed! Try again'
                })
    else:
        return render(request, 'my_auth/login.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('my_auth:login')


def register(request):
    form = MyRegisterForm()
    if request.POST:
        form = MyRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            user = MyUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('news:index')

    return render(request, 'my_auth/register.html', {'form': form})

from django.contrib.auth import login as django_login, logout as django_logout
from django.shortcuts import redirect

from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from my_auth.api.serializers import UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer
from my_auth.models import MyUser


class LoginAuthToken(ObtainAuthToken):
    serializer_class = UserLoginSerializer


def logout(request):
    django_logout(request)
    return redirect('my_auth:login')


class RegisterAuthToken(ObtainAuthToken, CreateModelMixin):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        create_response = super().create(request, *args, **kwargs)
        email = create_response.data.get('email')
        user = MyUser.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response({'token': token.key})


class UserProfileAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return MyUser.objects.filter(id=self.request.user.id)

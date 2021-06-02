from django.contrib.auth import login as django_login

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from my_auth.api.serializers import UserLoginSerializer, UserRegisterSerializer
from my_auth.models import MyUser


class LoginAuthToken(ObtainAuthToken):
    serializer_class = UserLoginSerializer


class RegisterAuthToken(ObtainAuthToken, CreateModelMixin):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        create_response = super().create(request, *args, **kwargs)
        email = create_response.data.get('email')
        user = MyUser.objects.get(email=email)
        token = Token.objects.get(user=user)
        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response({'token': token.key})

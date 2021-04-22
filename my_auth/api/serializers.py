from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from my_auth.models import MyUser


class UserLoginSerializer(AuthTokenSerializer):
    username = None
    email = serializers.EmailField(
        label=_("Email"),
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserRegisterSerializer(UserLoginSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        if email and password and first_name and last_name:
            if MyUser.objects.filter(email=email).exists():
                msg = _('User with such email is already registered.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "email", "password", "first name" and "last name".')
            raise serializers.ValidationError(msg, code='authorization')

        return attrs

    def create(self, validated_data):
        user = MyUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

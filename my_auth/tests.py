import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from my_auth.models import MyUser


@pytest.mark.django_db
def test_register():
    client = APIClient()
    test_post_data = {
        'email': 'test@m.ru',
        'password': 'pass5678',
        'first_name': 'Firstname',
        'last_name': 'Lastname'
    }

    response = client.post(
        path=reverse('register'),
        data=test_post_data,
        format='json'
    )
    token = Token.objects.get(user=MyUser.objects.get(email='test@m.ru'))
    assert(response.status_code == status.HTTP_200_OK)
    assert(token.key == response.data['token'])

    repeated_request_response = client.post(
        path=reverse('register'),
        data=test_post_data,
        format='json'
    )
    assert(repeated_request_response.status_code == status.HTTP_400_BAD_REQUEST)


@pytest.fixture
def test_user():
    user = MyUser.objects.create(
        email='test@m.ru',
        first_name='Firstname',
        last_name='Lastname'
    )
    user.set_password('pass5678')
    user.save()
    return user


@pytest.mark.django_db
def test_login(test_user):
    client = APIClient()
    response = client.post(
        path=reverse('login'),
        data={
            'email': 'test@m.ru',
            'password': 'pass5678',
        },
        format='json',
    )
    assert(response.status_code == status.HTTP_200_OK)
    token = Token.objects.get(user=test_user)
    assert(token.key == response.data['token'])

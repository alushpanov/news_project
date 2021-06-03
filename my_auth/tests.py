import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from pytest_drf import APIViewTest, AsUser, Returns200, UsesGetMethod, UsesPostMethod, UsesDetailEndpoint
from pytest_lambda import lambda_fixture, static_fixture

from my_auth.api.views import RegisterAuthToken
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


# test_user = lambda_fixture(
#     lambda: MyUser.objects.create(
#         email='test@m.ru',
#         # password='12345678',
#         first_name='Firstname',
#         last_name='Lastname'
#     ).set_password('12345678')
# )

# @pytest.fixture
# def test_user():
#     user = MyUser.objects.create(
#         email='test@m.ru',
#         # password='12345678',
#         first_name='Firstname',
#         last_name='Lastname'
#     )
#     user.set_password('pass5678')
#     return user


# @pytest.mark.django_db
# def test_login(test_user):
#     client = APIClient()
#     response = client.post(
#         path=reverse('login'),
#         data={
#             'email': 'test@m.ru',
#             'password': 'pass5678',
#         },
#         format='json',
#     )
#     print('RESPONSE DATA:')
#     print(response.data)
#     assert(response.status_code == status.HTTP_200_OK)
#     token = Token.objects.get(user=test_user)
#     assert(token.key == response.data['token'])


# class TestLogin(
#     APIViewTest,
#     UsesPostMethod,
#     # Returns200,
#     # AsUser('test_user')
# ):
#     url = lambda_fixture(lambda: reverse('login'))
#     # data = static_fixture({
#     #     'email': 'test@m.ru',
#     #     'password': '12345678',
#     # })
#
#     @pytest.fixture
#     def data(self):
#         return {
#             'email': 'test@m.ru',
#             'password': '12345678',
#         }
#
#     @pytest.mark.django_db
#     def test_login(self, json, test_user):
#         # u = MyUser.objects.get(email='test@m.ru')
#         # print(u.password)
#         token = Token.objects.get(user=test_user)
#         expected = {
#             'token': token.key
#         }
#         actual = json
#         assert(expected == actual)

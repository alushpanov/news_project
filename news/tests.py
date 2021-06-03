import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from pytest_assert_utils import assert_model_attrs
from pytest_common_subject import precondition_fixture
from pytest_drf import (
    APIViewTest,
    AsUser,
    AsAnonymousUser,
    ViewSetTest,
    Returns200,
    Returns201,
    Returns204,
    UsesGetMethod,
    UsesDeleteMethod,
    UsesDetailEndpoint,
    UsesListEndpoint,
    UsesPatchMethod,
    UsesPutMethod,
    UsesPostMethod,
)
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture, static_fixture

from my_auth.models import MyUser
from news.api.views import like
from news.models import Article, Category


def express_category(category):
    return {'name': category.name}

express_categories = pluralized(express_category)


@pytest.fixture
def test_user():
    user = MyUser.objects.create(
        email='test@m.ru',
        first_name='Firstname',
        last_name='Lastname'
    )
    user.set_password('pass5678')
    return user


@pytest.fixture
def test_category(test_user):
    return Category.objects.create(name='Test category', author=test_user)


@pytest.fixture
def test_categories(test_user):
    return [
        Category.objects.create(name='Category 1', author=test_user),
        Category.objects.create(name='Category 2', author=test_user)
    ]


class TestCategoryViewSet(ViewSetTest):
    list_url = lambda_fixture(
        lambda: url_for('category-list')
    )

    detail_url = lambda_fixture(
        lambda category: url_for('category-detail', category.pk)
    )

    @pytest.mark.django_db
    class TestList(
        AsUser('test_user'),
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        categories = lambda_fixture(test_categories)

        def test_it_returns_categories(self, categories, json):
            expected = express_categories(sorted(categories, key=lambda category: category.id))
            actual = json
            assert(expected == actual)


    @pytest.mark.django_db
    class TestCreate(
        AsUser('test_user'),
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        post_data = {'name': 'Test category'}
        data = static_fixture(post_data)

        initial_category_names = precondition_fixture(
            lambda: set(Category.objects.values_list('name', flat=True))
        )

        def test_it_creates_category(self, initial_category_names, json):
            expected = initial_category_names | {json['name']}
            actual = set(Category.objects.values_list('name', flat=True))
            assert expected == actual


    @pytest.mark.django_db
    class TestRetrieve(
        AsUser('test_user'),
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        category = lambda_fixture(test_category)

        def test_it_returns_category(self, category, json):
            expected = express_category(category)
            actual = json
            assert(expected == actual)


    @pytest.mark.django_db
    class TestUpdate(
        AsUser('test_user'),
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        category = lambda_fixture(test_category)

        post_data = {'name': 'Category updated'}
        data = static_fixture(post_data)

        def test_it_updates_category(self, data, category):
            category.refresh_from_db()
            expected = data
            assert_model_attrs(category, expected)


    @pytest.mark.django_db
    class TestDestroy(
        AsUser('test_user'),
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns204,
    ):
        category = lambda_fixture(test_category)

        initial_category_ids = precondition_fixture(
            lambda category: set(Category.objects.values_list('id', flat=True))
        )

        def test_it_deletes_category(self, initial_category_ids, category):
            expected = initial_category_ids - {category.id}
            actual = set(Category.objects.values_list('id', flat=True))
            assert(expected == actual)


# class TestLike(APIViewTest, AsUser('test_user'), UsesPostMethod):
#     url = lambda_fixture(lambda: reverse(like))
#
#     test_article = lambda_fixture(
#         lambda: Article.objects.create(title='Test title', text='Test text', author=test_user())
#     )
#
#     @pytest.fixture
#     def test_article(self, test_user):
#         return Article.objects.create(title='Test title', text='Test text', author=test_user)
#
#     # post_data = {'object_type': 'Article', 'object_id': test_article().id}
#     # data = static_fixture(post_data)
#
#     @pytest.fixture
#     def data(self, test_article):
#         return {
#             'object_type': 'Article',
#             'object_id': test_article.id,
#         }
#
#     @pytest.mark.django_db
#     def test_like(self, json):
#         pass
#         # print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
#         # print(self.client)
#         # assert(2 > 40)


# @pytest.fixture
# def test_article(test_user):
#     return Article.objects.create(title='Test title', text='Test text', author=test_user)
#
#
# @pytest.mark.django_db
# def test_like(test_user, test_article):
#     client = APIClient()
#     client.force_authenticate(test_user)
#     response = client.post(
#         path='/api/news/likes/',
#         data={
#             'object_id': test_article.id,
#             'object_type': 'Article'
#         },
#         format='json',
#     )
#     assert(response.status_code == status.HTTP_201_CREATED)

    # client.force_authenticate(create_test_user)
    # client.force_login(create_test_user)
    # response = client.post(
    #     path='/api/news/likes/',
    #     data={
    #         'object_id': '42',
    #         'content_type': 'Comment'
    #     },
    #     format='json',
    # )
    # print(response.data)
    # print(response.status_code)
    # assert(3 > 7)
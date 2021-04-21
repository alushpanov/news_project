from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_auth.models import MyUser
from news.api.serializers import AnalyticSerializer, ArticleSerializer, CategorySerializer
from news.models import Article, Category


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated])
def get_analytics(request):
    analytics_dict = {
        'most_liked_article_id': Article.objects.get_most_liked_article().id,
        'most_liked_article_title': Article.objects.get_most_liked_article().title,
        'most_commented_article_id': Article.objects.get_most_commented_article().id,
        'most_commented_article_title': Article.objects.get_most_commented_article().title,
        'author_with_max_comments_fullname': MyUser.objects.get_user_with_max_comments().first_name[:-1]
                                             + ' ' + MyUser.objects.get_user_with_max_comments().last_name[:-1],
        'author_with_max_comments_id': MyUser.objects.get_user_with_max_comments().id,
        'articles_with_images': Article.objects.count_articles_with_images(),
        'articles_with_no_views': Article.objects.count_articles_with_no_views(),
        'articles_with_no_likes': Article.objects.count_articles_with_no_likes(),
        'date_max_articles_posted': Article.objects.get_date_max_articles_posted()['creation_date'],
        'max_articles_posted': Article.objects.get_date_max_articles_posted()['articles_count'],
        'date_min_articles_posted': Article.objects.get_date_min_articles_posted()['creation_date'],
        'min_articles_posted': Article.objects.get_date_min_articles_posted()['articles_count']
    }
    serializer = AnalyticSerializer(analytics_dict)
    return Response(serializer.data)

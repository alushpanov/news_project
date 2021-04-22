from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from my_auth.models import MyUser
from news.api import serializers as news_serializers
from news.models import Article, Category, Comment, Like
from news.permissions import IsAuthorOrReadOnly, IsUserWhoLiked


class ArticleViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = news_serializers.ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Article.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = news_serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    filter_fields = ['article_id']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = news_serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class UserProfileAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = news_serializers.UserProfileSerializer

    def get_queryset(self):
        return MyUser.objects.filter(id=self.request.user.id)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[permissions.IsAuthenticated])
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
    serializer = news_serializers.AnalyticSerializer(analytics_dict)
    return Response(serializer.data)


@api_view(http_method_names=['POST', 'DELETE'])
@permission_classes(permission_classes=[permissions.IsAuthenticated])
def like(request):
    if request.method == 'POST':
        try:
            instance_id = request.query_params['article_id']
            content_type = Article
        except KeyError:
            instance_id = request.query_params['comment_id']
            content_type = Comment

        like_obj, created = Like.objects.get_or_create(
            user=request.user,
            object_id=instance_id,
            content_type_id=ContentType.objects.get_for_model(content_type).id
        )
        serializer = news_serializers.LikeSerializer(like_obj)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        like_obj = get_object_or_404(Like, id=request.query_params['id'])
        # if request.user.has_perm(IsUserWhoLiked, like_obj):  # always False
        if request.user == like_obj.user:
            like_obj.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

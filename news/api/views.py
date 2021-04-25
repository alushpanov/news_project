from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from my_auth.models import MyUser
from news.api import serializers as news_serializers
from news.models import Article, Category, Comment, Like
from news.permissions import IsAuthorOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = news_serializers.ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Article.objects.a_num_likes()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = news_serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Comment.objects.a_num_likes()
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
    analytics_dict = Article.objects.get_analytics_dict()
    serializer = news_serializers.AnalyticSerializer(analytics_dict)
    return Response(serializer.data)


@api_view(http_method_names=['POST', 'DELETE'])
@permission_classes(permission_classes=[permissions.IsAuthenticated])
def like(request):
    if request.method == 'POST':
        serializer = news_serializers.LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        like_obj = get_object_or_404(Like, id=request.query_params['id'])
        if request.user == like_obj.user:
            like_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

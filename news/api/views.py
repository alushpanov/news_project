from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from news.api.serializers import ArticleSerializer, CommentSerializer, LikeSerializer
from news.models import Article, Comment, Like
from news.permissions import IsAuthorOrReadOnly, IsUserWhoLiked


class ArticleViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Article.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    filter_fields = ['article_id']


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
        serializer = LikeSerializer(like_obj)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        like_obj = get_object_or_404(Like, id=request.query_params['id'])
        # if request.user.has_perm(IsUserWhoLiked, like_obj):  # always False
        if request.user == like_obj.user:
            like_obj.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

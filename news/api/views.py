from django.contrib.contenttypes.models import ContentType

from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from news.api.serializers import ArticleSerializer, CommentSerializer, LikeSerializer
from news.models import Article, Comment, Like


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


@api_view(http_method_names=['POST', 'DELETE'])  # uniqueness of likes
@permission_classes(permission_classes=[permissions.IsAuthenticated, IsAuthorOrReadOnly])
def like(request):
    if request.method == 'POST':
        try:
            instance_id = request.query_params['article_id']
            content_type = Article
        except KeyError:
            instance_id = request.query_params['comment_id']
            content_type = Comment

        like_obj = Like.objects.create(
            user=request.user,
            object_id=instance_id,
            content_type_id=ContentType.objects.get_for_model(content_type).id
        )
        serializer = LikeSerializer(like_obj)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        pass

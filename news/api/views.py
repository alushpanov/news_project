from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from news.api.serializers import ArticleSerializer, CommentSerializer
from news.models import Article, Comment


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

    def get_queryset(self):
        return Comment.objects.all()

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset().filter(article_id=request.query_params['article_id'])
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data)


@api_view(http_method_names=['POST', 'DELETE'])
def like(request):
    pass

from rest_framework import permissions, viewsets
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
    queryset = Article.objects.all()
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def list(self, request, *args, **kwargs):
        query_set = self.queryset.filter(article_id=request.data['article'])
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data)

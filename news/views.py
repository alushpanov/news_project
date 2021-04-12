from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser

from news.api.serializers import ArticleSerializer
from news.models import Article


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
    parser_classes = [JSONParser, MultiPartParser, ]  # FileUploadParser
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser, MultiPartParser

from news.api.serializers import ArticleSerializer, CategorySerializer
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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from news.api.serializers import ArticleSerializer
from news.models import Article


@api_view(http_method_names=['PATCH'])
@permission_classes(permission_classes=[IsAuthenticated])
def like_article(request, pk):
    article = Article.objects.get(pk=pk)
    article.likes += 1
    article.save()

    serializer = ArticleSerializer(instance=article)
    return Response(serializer.data)

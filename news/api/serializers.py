from rest_framework import serializers

from news.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'text', 'image', 'categories']

    def create(self, validated_data):
        article = Article.objects.create(
            title=validated_data['title'],
            text=validated_data['text'],
            author_id=self.context['author_id'],
        )
        return article

import base64
from binascii import Error as BinASCIIError

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from news.models import Article, Category, Comment
from news.signals import replace_image


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        """
        It checks for the type of the data and either decodes it from
        base64 or directly saves the file.
        """

        data_name = data['name']
        data_content = data['content']
        if isinstance(data_content, str):
            try:
                decoded_file = base64.b64decode(data_content)
            except BinASCIIError:
                raise ValidationError('Corrupted file data, please try again.')
            data_content = ContentFile(decoded_file, name=f'{data_name}')
        else:
            raise ValidationError(
                '%(value)s is not a valid file format' % type(data_content),
                code='invalid',
            )
        return super().to_internal_value(data_content)


class ArticleSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Article
        fields = ['title', 'text', 'image', 'categories']

    def create(self, validated_data):
        article = Article(author_id=self.context['request'].user.id)
        super().update(article, validated_data)
        article.categories.set(validated_data['categories'])
        return article

    def validate_categories(self, data):
        if len(data) > 3:
            raise ValidationError('No more than 3 categories allowed!')
        return data

    def update(self, instance, validated_data):
        old_image_name = instance.image.name.split('/')[-1]
        new_image_name = self.context['request'].data['image']['name']
        if old_image_name != new_image_name:
            replace_image.send(sender=Article, instance=instance)
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'article', 'text']

    def create(self, validated_data):
        comment = Comment(
            author=self.context['request'].user,
            article_id=validated_data['article']
        )
        super().update(comment, validated_data)
        return comment

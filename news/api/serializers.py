import base64
from binascii import Error as BinASCIIError

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from news.models import Article, Category, Comment, Like
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
    num_likes = serializers.IntegerField(default=0)  # annotation is performed in ArticleManager

    class Meta:
        model = Article
        fields = ['title', 'text', 'image', 'categories', 'num_likes']

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
        try:
            new_image_name = self.context['request'].data['image']['name']
            old_image_name = instance.image.name.split('/')[-1]
            if old_image_name != new_image_name:
                replace_image.send(sender=Article, instance=instance)
        except KeyError:
            pass
        validated_data['num_likes'] = instance.num_likes
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    article = serializers.PrimaryKeyRelatedField(read_only=True)
    num_likes = serializers.IntegerField(default=0)  # annotation is performed in CommentManager

    class Meta:
        model = Comment
        fields = ['author', 'article', 'text', 'num_likes']

    def create(self, validated_data):
        comment = Comment(
            author=self.context['request'].user,
            article_id=self.context['request'].query_params['article_id']
        )
        super().update(comment, validated_data)
        return comment

    def update(self, instance, validated_data):
        validated_data['num_likes'] = instance.num_likes
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        category = Category(author_id=self.context['request'].user.id)
        super().update(category, validated_data)
        return category


class AnalyticSerializer(serializers.Serializer):
    most_liked_article_id = serializers.IntegerField()
    most_liked_article_title = serializers.CharField()
    most_commented_article_id = serializers.IntegerField()
    most_commented_article_title = serializers.CharField()
    author_with_max_comments_fullname = serializers.CharField()
    author_with_max_comments_id = serializers.IntegerField()
    articles_with_images = serializers.IntegerField()
    articles_with_no_views = serializers.IntegerField()
    articles_with_no_likes = serializers.IntegerField()
    date_max_articles_posted = serializers.DateField()
    max_articles_posted = serializers.IntegerField()
    date_min_articles_posted = serializers.DateField()
    min_articles_posted = serializers.IntegerField()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'object_id']

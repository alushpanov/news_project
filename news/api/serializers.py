from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from my_auth.models import MyUser
from news.api.fields import Base64ImageField
from news.models import Article, Category, Comment, Like
from news.signals import replace_image


class ArticleSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    num_likes = serializers.IntegerField(default=0)  # annotation is performed in ArticleQuerySet

    class Meta:
        model = Article
        fields = ['title', 'text', 'image', 'categories', 'num_likes']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data.pop('num_likes')
        categories = validated_data.pop('categories')
        article = super().create(validated_data)
        article.categories.set(categories)
        return article

    def validate_categories(self, data):
        if len(data) > 3:
            raise ValidationError('No more than 3 categories allowed!')
        return data

    def update(self, instance, validated_data):
        if 'image' in self.context['request'].data:
            replace_image.send(sender=Article, instance=instance)
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    article = serializers.PrimaryKeyRelatedField(read_only=True)
    num_likes = serializers.IntegerField(default=0)  # annotation is performed in CommentQuerySet

    class Meta:
        model = Comment
        fields = ['author', 'article', 'text', 'num_likes']

    def create(self, validated_data):
        validated_data.pop('num_likes')
        validated_data['author'] = self.context['request'].user
        validated_data['article_id'] = self.context['request'].query_params['article_id']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'first_name', 'last_name', 'email']


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
    content_type = serializers.HiddenField(default=None)

    class Meta:
        model = Like
        fields = ['object_id', 'content_type']

    def validate(self, attrs):
        try:
            object_type = apps.get_model('news', self.initial_data['object_type'])
        except LookupError:
            raise ValidationError('There is no such model')

        if object_type is not Article and object_type is not Comment:
            raise ValidationError('Only Article or Comment can be liked')

        if not object_type.objects.filter(id=attrs['object_id']).exists():
            raise ValidationError('There is no such instance')

        attrs['content_type'] = ContentType.objects.get_for_model(object_type)
        return attrs

    def create(self, validated_data):
        try:
            like_to_create = Like.objects.get(**validated_data)
            return like_to_create
        except Like.DoesNotExist:
            return super().create(validated_data)

from rest_framework import serializers


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

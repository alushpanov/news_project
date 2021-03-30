from django.conf import settings
from django.db import models

from news.managers import ArticleManager
from news.storage import article_image_path


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=article_image_path, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    archived = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    objects = ArticleManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.IntegerField(default=0)

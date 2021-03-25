from django.conf import settings
from django.db import models

from news.storage import article_image_path


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=article_image_path, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    archived = models.BooleanField(default=False)

    objects = ArticleManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.title

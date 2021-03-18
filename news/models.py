from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)

    def __str__(self):
        return self.title

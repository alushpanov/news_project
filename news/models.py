from django.db import models
from django.contrib.auth.models import User

from news_project import settings


class Article(models.Model):
    title = models.CharField(max_length=100)
    article_text = models.TextField()
    created_on = models.DateField()  # auto_now_add=True
    last_modified = models.DateField(auto_now=True)
    image = models.ImageField('', null=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=20)
    articles = models.ManyToManyField(Article, related_name='categories')

    def __str__(self):
        return self.name

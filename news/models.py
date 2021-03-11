# import os
from django.db import models
from django.contrib.auth.models import User

from news_project import settings


class Article(models.Model):
    title = models.CharField(max_length=100)
    article_text = models.TextField()
    created_on = models.DateField()
    # image = models.FilePathField(path=os.path.join(settings.BASE_DIR))
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

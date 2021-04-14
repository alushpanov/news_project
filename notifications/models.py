from django.db import models

from news.models import Article


class Notification(models.Model):
    text = models.CharField(max_length=100)
    article = models.ForeignKey(Article, related_name='notifications', on_delete=models.CASCADE)

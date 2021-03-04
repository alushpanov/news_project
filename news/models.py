from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)


class News(models.Model):
    title = models.CharField(max_length=100)
    news_text = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    # image = models.FilePathField
    author = models.ForeignKey(Author, on_delete=models.PROTECT)

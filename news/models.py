from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    article_text = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    # image = models.FilePathField
    author = models.ForeignKey(Author, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

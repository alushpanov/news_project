from django.contrib import admin

from news.forms.article import ArticleAdminForm
from news.models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

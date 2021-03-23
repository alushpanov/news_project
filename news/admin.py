from django.contrib import admin

from news.forms.article import ArticleAdminForm
from news.models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'archived')

    def get_queryset(self, request):
        return Article.all_articles.order_by('-created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

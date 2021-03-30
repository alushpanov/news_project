from django.contrib import admin

from news.forms.article import ArticleAdminForm
from news.models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'archived')

    def get_queryset(self, request):
        return Article.all_objects.order_by('-created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

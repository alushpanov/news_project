from django.contrib import admin
from django.db.models import Count

from news.forms.article import ArticleAdminForm
from news.models import Article, Category, Comment, Like


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'num_likes', 'archived')
    list_filter = ('author', )
    readonly_fields = ('created_at', )

    def get_queryset(self, request):
        return Article.all_objects.annotate(num_likes=Count('likes')).order_by('-created_at')

    def num_likes(self, obj):
        return obj.num_likes


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from news.api import views as api_views


router = DefaultRouter()
router.register(r'articles', api_views.ArticleViewSet, 'article')
router.register(r'comments', api_views.CommentViewSet, 'comment')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', api_views.get_analytics),
    path('likes/', api_views.like),
]

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from news.api import views as api_views


router = DefaultRouter()
router.register(r'articles', api_views.ArticleViewSet)
router.register(r'comments', api_views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from news import views


router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'categories', views.CategoryViewSet)

app_name = 'news'
urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import include, path

from rest_framework.routers import DefaultRouter
from news import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

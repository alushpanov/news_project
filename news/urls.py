from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mynews/', views.UserArticleListView.as_view(), name='user_articles'),
    path('create/', views.create, name='create_article'),
    path('mynews/<int:pk>/archive/', views.archive_article, name='archive_article'),
    path('mynews/<int:pk>/', views.ArticleUpdateView.as_view(), name='update_article'),
]

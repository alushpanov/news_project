from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.create, name='create'),
    path('mynews/', views.MyNewsView.as_view(), name='user_news'),
    path('mynews/<int:pk>/archive/', views.archive_article, name='archive_article'),
    path('mynews/<int:pk>/', views.ArticleUpdate.as_view(), name='edit'),
]

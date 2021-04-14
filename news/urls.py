from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('<int:pk>/', views.like_article),
]

from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.create, name='create'),
    path('mynews/', views.MyNewsView.as_view(), name='my_news'),
]

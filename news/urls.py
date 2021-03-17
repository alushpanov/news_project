from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('', views.index_view, name='index'),
]

from django.urls import path
from my_auth import views

app_name = 'my_auth'
urlpatterns = [
    path('', views.index_view, name='index'),
]

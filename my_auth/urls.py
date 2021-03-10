from django.urls import path
from my_auth import views

app_name = 'my_auth'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
]

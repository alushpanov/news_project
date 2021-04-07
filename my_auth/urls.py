from django.urls import path

from my_auth import views


app_name = 'my_auth'
urlpatterns = [
    path('register/', views.RegisterAuthToken.as_view(), name='register'),
    path('login/', views.LoginAuthToken.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]

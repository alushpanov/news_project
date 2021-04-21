from django.urls import path

from my_auth.api import views as api_views


urlpatterns = [
    path('register/', api_views.RegisterAuthToken.as_view(), name='register'),
    path('login/', api_views.LoginAuthToken.as_view(), name='login'),
]

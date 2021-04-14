from django.urls import path, include


urlpatterns = [
    path('auth/', include('my_auth.urls')),
    path('articles/', include('news.urls')),
]

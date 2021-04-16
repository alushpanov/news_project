from django.urls import path, include


urlpatterns = [
    path('news/', include('news.api.urls')),
    path('notifications/', include('notifications.api.urls')),
]

from django.urls import path, include


urlpatterns = [
    path('auth/', include('my_auth.api.urls')),
    path('notifications/', include('notifications.api.urls')),
]

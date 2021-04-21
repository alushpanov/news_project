from django.urls import path

from notifications.api import views as api_views


urlpatterns = [
    path('', api_views.NotificationsListAPIView.as_view()),
]

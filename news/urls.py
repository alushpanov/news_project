from django.contrib.auth.decorators import login_required
from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('', login_required(views.IndexView.as_view()), name='index'),
]

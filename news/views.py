from django.shortcuts import render
from django.http import HttpResponse
from news.models import Article

def index(request):
    articles = Article.objects.all().order_by('-created_on')
    return render(request, 'index.html', {'articles': articles})

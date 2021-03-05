from django.shortcuts import render
from django.views import generic

from news.models import Article


class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Article.objects.all().order_by('-created_on')


class DetailView(generic.DetailView):
    model = Article
    template_name = 'detail.html'

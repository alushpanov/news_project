from django.shortcuts import render, redirect
from django.views import generic
from datetime import date

from news.models import Article
from news.forms import ArticleForm


class IndexView(generic.ListView):
    template_name = 'news/index.html'

    def get_queryset(self):
        return Article.objects.all().order_by('-created_on')


def create(request):
    form = ArticleForm()
    if request.POST:
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data.get('title'),
                article_text=form.cleaned_data.get('article_text'),
                # categories=form.cleaned_data.get('categories'),
                # image=form.cleaned_data.get('image'),
                created_on=date.today(),
                author=request.user
            )
            # article.categories.add(form.cleaned_data.get('categories'))
            article.save()
            return redirect('news:index')
    context = {
        'form': form
    }
    return render(request, 'news/create.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import generic

from news.forms.article import ArticleForm
from news.models import Article


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'news/index.html'

    def get_queryset(self):
        return Article.objects.all().order_by('-created_at')


def create(request):
    form = ArticleForm()
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            categories = form.cleaned_data.pop('categories')
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            article.categories.set(categories)
            return redirect('news:index')
    return render(request, 'news/create.html', {'form': form})


class MyNewsView(generic.ListView):
    template_name = 'news/user.html'

    def get_queryset(self):
        return Article.objects.filter(author_id=self.request.user.id)


def edit(request, pk):  # turn to class view
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('news:my_news')
    return render(request, 'news/edit.html', {'form': form})


def archive(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.archived = True
    article.save()
    return redirect('news:my_news')

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from news.forms.article import ArticleForm
from news.models import Article


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'news/index.html'
    paginate_by = 100

    def get_queryset(self):
        return Article.objects.all().order_by('-created_at')


class UserArticleListView(generic.ListView):
    template_name = 'news/user_articles.html'

    def get_queryset(self):
        return Article.objects.filter(author_id=self.request.user.id).order_by('-created_at')


def create_article(request):
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
    return render(request, 'news/create_article.html', {'form': form})


class ArticleUpdateView(generic.UpdateView):
    model = Article
    template_name = 'news/update_article.html'
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('news:user_articles')


def archive_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.archived = True
    article.save()
    return redirect('news:user_articles')


class SearchListView(generic.ListView):
    model = Article
    template_name = 'news/index.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Article.objects.filter(
            Q(title__icontains=query)
            | Q(text__icontains=query)
            | Q(author__first_name__icontains=query)
            | Q(author__last_name__icontains=query)
            | Q(comments__author__first_name__icontains=query)
            | Q(comments__author__last_name__icontains=query)
            | Q(comments__text__icontains=query)
        )

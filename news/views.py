from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
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
        return Article.objects.filter(author_id=self.request.user.id).order_by('-created_at')


class ArticleUpdate(generic.UpdateView):
    model = Article
    template_name = 'news/edit.html'
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('news:user_news')


def archive_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.archived = True
    article.save()
    return redirect('news:user_news')

# COMBINE CLASS VIEWS INTO ONE
# TemplateView?

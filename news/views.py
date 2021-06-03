from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from my_auth.models import MyUser
from news.forms.article import ArticleForm
from news.models import Article


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'news/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.a_num_likes().order_by('-created_at')


@method_decorator(login_required, name='dispatch')
class UserArticleListView(generic.ListView):
    template_name = 'news/user_articles.html'

    def get_queryset(self):
        return Article.objects.filter(author_id=self.request.user.id).order_by('-created_at')


@login_required()
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


@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(generic.UpdateView):
    model = Article
    template_name = 'news/update_article.html'
    form_class = ArticleForm

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('news:user_articles')


def archive_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.archived = True
    article.save()
    return redirect('news:user_articles')


class AnalyticsTemplateView(generic.TemplateView):
    template_name = 'news/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_liked_article'] = Article.objects.get_most_liked_article()
        context['most_commented_article'] = Article.objects.get_most_commented_article()
        context['most_commenting_user'] = MyUser.objects.get_user_with_max_comments()
        context['amount_of_articles_with_images'] = Article.objects.count_articles_with_images()
        context['amount_of_articles_with_no_views'] = Article.objects.count_articles_with_no_views()
        context['amount_of_articles_with_no_likes'] = Article.objects.count_articles_with_no_likes()

        date_with_max_articles = Article.objects.get_date_max_articles_posted()
        context['date_with_max_articles'] = date_with_max_articles['creation_date']
        context['max_articles'] = date_with_max_articles['articles_count']

        date_with_min_articles = Article.objects.get_date_min_articles_posted()
        context['date_with_min_articles'] = date_with_min_articles['creation_date']
        context['min_articles'] = date_with_min_articles['articles_count']

        return context


class SearchArticleListView(generic.ListView):
    model = Article
    template_name = 'news/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Article.objects.search_query(query)

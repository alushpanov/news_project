from django.shortcuts import redirect, render

from news.models import Article


def index_view(request):
    if request.user.is_authenticated:
        article_list = Article.objects.all().order_by('-created_at')
        return render(request, 'news/index.html', {'article_list': article_list})
    else:
        return redirect('my_auth:login')

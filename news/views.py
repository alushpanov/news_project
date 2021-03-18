from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from news.models import Article


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'news/index.html'

    def get_queryset(self):
        return Article.objects.all().order_by('-created_at')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

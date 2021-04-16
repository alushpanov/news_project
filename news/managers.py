from django.db.models import Count, Manager, Q


class ArticleManager(Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(num_likes=Count('likes')).filter(archived=False)

    def search_query(self, query):
        splitted_query = query.split(' ')
        q = Q()
        for s in splitted_query:
            q |= Q(title__icontains=s)\
                 | Q(text__icontains=s)\
                 | Q(comments__text__icontains=s)\
                 | Q(author__first_name__istartswith=s)\
                 | Q(author__last_name__istartswith=s)\
                 | Q(comments__author__first_name__istartswith=s)\
                 | Q(comments__author__last_name__istartswith=s)

        return self.get_queryset().filter(q).order_by('-created_at')


class CommentManager(Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(num_likes=Count('likes'))

from django.db.models import Count, Max, Min, Q, QuerySet
from django.db.models.fields import DateField
from django.db.models.functions import Cast


class ArticleQuerySet(QuerySet):
    def get_queryset(self):
        return super().filter(archived=False)

    def a_num_likes(self):
        return self.get_queryset().annotate(num_likes=Count('likes'))

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
        return self.get_queryset().filter(q).distinct().order_by('-created_at')

    def get_most_liked_article(self):
        max_likes = self.get_queryset().aggregate(Max('likes'))
        return self.get_queryset().filter(likes=max_likes['likes__max']).first()

    def get_most_commented_article(self):
        qs_comments_counted = self.get_queryset().annotate(comments_count=Count('comments'))
        return qs_comments_counted.order_by('comments_count').last()

    def count_articles_with_images(self):
        return self.get_queryset().exclude(image__exact='').count()

    def count_articles_with_no_views(self):
        return self.get_queryset().filter(views=0).count()

    def count_articles_with_no_likes(self):
        return self.get_queryset().filter(likes=0).count()

    def _get_queryset_with_dates_counted(self):
        qs_dates_counted = self.get_queryset() \
            .annotate(creation_date=Cast('created_at', DateField())) \
            .values('creation_date') \
            .annotate(articles_count=Count('id'))
        return qs_dates_counted

    def get_date_max_articles_posted(self):
        qs_dates_counted = self._get_queryset_with_dates_counted()
        max_articles_posted = qs_dates_counted.aggregate(Max('articles_count'))
        filtered_max_articles = qs_dates_counted.filter(articles_count=max_articles_posted['articles_count__max'])
        if len(filtered_max_articles) > 0:
            return filtered_max_articles[0]  # .first()
        else:
            raise ValueError('db is empty')

    def get_date_min_articles_posted(self):
        qs_dates_counted = self._get_queryset_with_dates_counted()
        min_articles_posted = qs_dates_counted.aggregate(Min('articles_count'))
        filtered_min_articles = qs_dates_counted.filter(articles_count=min_articles_posted['articles_count__min'])
        if len(filtered_min_articles) > 0:
            return filtered_min_articles[0]  # .first()
        else:
            raise ValueError('db is empty')


class CommentQuerySet(QuerySet):
    def get_queryset(self):
        return super().all()

    def a_num_likes(self):
        return self.get_queryset().annotate(num_likes=Count('likes'))

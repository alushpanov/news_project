from django.db.models import Manager, Max, Count


class ArticleManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)

    def get_most_liked_article(self):
        max_likes = self.get_queryset().aggregate(Max('likes'))
        return self.get_queryset().filter(likes=max_likes['likes__max']).first()

    def get_most_commented_article(self):
        qs_comments_counted = self.get_queryset().annotate(comments_count=Count('comments'))
        max_commented = qs_comments_counted.aggregate(Max('comments_count'))
        return qs_comments_counted.filter(comments_count=max_commented['comments_count__max']).first()

    def count_articles_with_images(self):
        return self.get_queryset().exclude(image__exact='').count()

    def count_articles_with_no_views(self):
        return self.get_queryset().filter(views=0).count()

    def count_articles_with_no_likes(self):
        return self.get_queryset().filter(likes=0).count()

    def get_date_max_articles_posted(self):
        pass

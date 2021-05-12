import time
from random import randint

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.urls import reverse

from my_auth.models import MyUser
from news.models import Article, Category, Like
from news_project.celery import app as celery_app
from notifications.services import create_notification


@celery_app.task
def notify(instance_id, instance_class_str, sender_class_str):
    instance_class = apps.get_model(instance_class_str)
    instance = instance_class.objects.get(id=instance_id)
    notification = create_notification(instance, apps.get_model(sender_class_str))
    notification.save()


@celery_app.task
def generate_random_articles():
    amount_of_articles = randint(0, 5)
    if amount_of_articles == 0:
        return

    category_for_generated, created = Category.objects.get_or_create(
        name='generated article',
        defaults={'author': MyUser.objects.random()}
    )

    bulk_likes = []
    for i in range(amount_of_articles):
        article = Article.objects.create(
            title=str(time.time()),
            text='Text of automatically generated article',
            author=MyUser.objects.random(),
            views=randint(0, 2000),
        )
        article.categories.set([category_for_generated.id])

        num_likes = randint(0, 20)
        for j in range(num_likes):
            like = Like(
                user=MyUser.objects.random(),
                content_type=ContentType.objects.get_for_model(Article),
                object_id=article.id,
            )
            bulk_likes.append(like)
    Like.objects.bulk_create(bulk_likes)


@celery_app.task
def send_emails_with_latest_news():
    latest_articles = Article.objects.get_articles_for_24_hours().order_by('-num_likes', '-views')
    three_most_popular = latest_articles[:3]
    domain = Site.objects.get_current().domain
    three_most_popular_urls = '\n'.join(
        [domain + reverse('article-detail', args=(k.id,)) for k in three_most_popular]
    )

    msg = 'Amount of articles published within 24 hours: {}\n' \
          'Check out the most popular ones:\n' \
          '{}'\
        .format(latest_articles.count(), three_most_popular_urls)

    latest_articles_subscribers = MyUser.objects.latest_articles_subscribers()
    send_mail(
        'LATEST NEWS!',
        msg,
        None,
        latest_articles_subscribers,
        fail_silently=False,
    )

import time
from random import randint

from django.apps import apps

from my_auth.models import MyUser
from news.models import Article
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

    bulk_articles = []
    for i in range(amount_of_articles):
        article = Article(
            title=str(time.time()),
            text='Text of automatically generated article',
            author=MyUser.objects.get(is_staff=True),
        )
        bulk_articles.append(article)
    Article.objects.bulk_create(bulk_articles)

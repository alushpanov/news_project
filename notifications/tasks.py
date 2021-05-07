import time
from random import randint

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

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
        author=MyUser.objects.get(is_staff=True),
    )

    bulk_articles = []
    for i in range(amount_of_articles):
        article = Article(
            title=str(time.time()),
            text='Text of automatically generated article',
            author=MyUser.objects.random(),
            views=randint(0, 2000),
        )
        bulk_articles.append(article)
    Article.objects.bulk_create(bulk_articles)

    generated_articles = Article.objects.all().order_by('-created_at')[:amount_of_articles]
    for article in generated_articles:
        article.categories.set([category_for_generated.id])

        num_likes = randint(0, 20)
        bulk_likes = []
        for i in range(num_likes):
            like = Like(
                user=MyUser.objects.random(),
                content_type=ContentType.objects.get_for_model(Article),
                object_id=article.id,
            )
            bulk_likes.append(like)
        Like.objects.bulk_create(bulk_likes)

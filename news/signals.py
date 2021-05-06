import os

from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from news.models import Article, Comment, Like
from notifications.tasks import notify


@receiver(post_delete, sender=Article)
def remove_image(sender, instance, **kwargs):
    if instance.image:
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.image.path))


@receiver(pre_save, sender=Article)
def replace_image(sender, instance, **kwargs):
    old_article = Article.objects.filter(id=instance.id).first()
    if old_article:
        if old_article.image and old_article.image != instance.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, old_article.image.path))


@receiver(post_save, sender=Like)
@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    sender_class_str = sender._meta.label
    instance_class_str = instance._meta.label
    notify.delay(instance.id, instance_class_str, sender_class_str)

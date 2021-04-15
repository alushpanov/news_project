import os

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from news.models import Article, Comment, Like
from notifications.models import Notification


@receiver(post_delete, sender=Article)
def remove_image(sender, instance, **kwargs):
    os.remove(os.path.join(settings.MEDIA_ROOT, instance.image.path))


@receiver(post_save, sender=Like)
@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    notification = Notification.create_from_instance(instance=instance, signal_sender=sender)
    notification.save()

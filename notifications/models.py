from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from news.models import Article, Like


class Notification(models.Model):
    text = models.CharField(max_length=100)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_from_instance(cls, instance, signal_sender):
        if signal_sender is Like:
            if instance.content_type.model_class() is Article:
                notification_text = '{} liked your article "{}"' \
                    .format(instance.user.email, instance.content_object.title)
            else:
                notification_text = '{} liked your comment to article "{}"' \
                    .format(instance.user.email, instance.content_object.article.title)

            notification_receiver = instance.content_object.author
            notification_sender = instance.user
        else:
            notification_text = '{} commented your article "{}"' \
                .format(instance.author.email, instance.article.title)
            notification_receiver = instance.article.author
            notification_sender = instance.author

        return cls(
            text=notification_text,
            receiver=notification_receiver,
            sender=notification_sender
        )

from news.models import Article, Comment, Like
from notifications.models import Notification


def create_notification(instance, signal_sender):
    if signal_sender is Like:
        if instance.content_type.model_class() is Article:
            notification_text = '{} liked your article "{}"' \
                .format(instance.user.email, instance.content_object.title)
        elif instance.content_type.model_class() is Comment:
            notification_text = '{} liked your comment to article "{}"' \
                .format(instance.user.email, instance.content_object.article.title)

        notification_receiver = instance.content_object.author
        notification_sender = instance.user
    elif signal_sender is Comment:
        notification_text = '{} commented your article "{}"' \
            .format(instance.author.email, instance.article.title)
        notification_receiver = instance.article.author
        notification_sender = instance.author

    return Notification(
        text=notification_text,
        receiver=notification_receiver,
        sender=notification_sender
    )

import os

from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import Signal

from news.models import Article


def remove_image(sender, instance, **kwargs):
    if instance.image:
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.image.path))


post_delete.connect(remove_image, sender=Article)

replace_image = Signal()
replace_image.connect(remove_image)

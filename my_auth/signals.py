from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from my_auth.models import MyUser


@receiver(post_save, sender=MyUser)
def create_token(sender, instance, **kwargs):
    Token.objects.get_or_create(user=instance)

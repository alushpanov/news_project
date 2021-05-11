import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from my_auth.managers import CustomUserManager


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Subscriptions(models.Model):
    latest_articles = models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions')

    class Meta:
        verbose_name_plural = 'subscriptions'

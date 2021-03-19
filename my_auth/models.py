import uuid
from django.db import models
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

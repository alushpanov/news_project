from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    text = models.CharField(max_length=100)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

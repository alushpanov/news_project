from django.apps import apps

from news_project.celery import app as celery_app
from notifications.services import create_notification


@celery_app.task
def notify(instance_id, instance_class_str, sender_class_str):
    instance_class = apps.get_model(instance_class_str)
    instance = instance_class.objects.get(id=instance_id)
    notification = create_notification(instance, apps.get_model(sender_class_str))
    notification.save()

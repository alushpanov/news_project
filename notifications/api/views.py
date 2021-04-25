from rest_framework import permissions
from rest_framework.generics import ListAPIView

from notifications.api.serializers import NotificationSerializer
from notifications.models import Notification
from notifications.permissions import IsReceiver


class NotificationsListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsReceiver]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

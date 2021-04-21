from rest_framework import permissions
from rest_framework.generics import ListAPIView

from notifications.models import Notification
from notifications.api.serializers import NotificationSerializer


class IsReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user


class NotificationsListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsReceiver]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

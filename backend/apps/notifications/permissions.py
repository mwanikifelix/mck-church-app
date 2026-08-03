from rest_framework.permissions import BasePermission

from apps.accounts.permissions import HasPermissionCode


class NotificationPermission(BasePermission):
    """Users only ever see/modify their own notifications."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.recipient_id == request.user.id or request.user.is_superuser


BroadcastPermission = HasPermissionCode("notifications.broadcast")

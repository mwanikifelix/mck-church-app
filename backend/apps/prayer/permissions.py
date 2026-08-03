from rest_framework.permissions import BasePermission

from apps.accounts.permissions import HasPermissionCode


class PrayerRequestPermission(BasePermission):
    """Any authenticated user can create. Viewing/editing a specific
    request requires being its submitter or holding prayer.manage."""

    manage_permission = HasPermissionCode("prayer.manage")

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if obj.submitter_id == user.id:
            return True
        return self.manage_permission().has_permission(request, view)

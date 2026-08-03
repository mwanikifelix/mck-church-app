from rest_framework.permissions import BasePermission

from apps.accounts.permissions import HasPermissionCode


class CounsellingRequestPermission(BasePermission):
    """Any authenticated user can create. Viewing/editing a specific
    request requires being its submitter or holding pastoral.view_all."""

    view_all_permission = HasPermissionCode("pastoral.view_all")

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if obj.user_id == user.id:
            return True
        return self.view_all_permission().has_permission(request, view)

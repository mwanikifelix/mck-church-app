from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.accounts.permissions import HasPermissionCode


class IsHBCGroupTreasurerLeaderOrManager(BasePermission):
    """Any authenticated member can read. Writing to a specific HBCGroup
    (including its treasurer/paybill fields) requires being that group's
    leader or treasurer, OR holding hbc.manage_members, OR superuser."""

    manage_permission = HasPermissionCode("hbc.manage_members")

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if obj.leader_id == request.user.id or obj.treasurer_id == request.user.id:
            return True
        return self.manage_permission().has_permission(request, view)

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.accounts.permissions import HasPermissionCode


class DonationPermission(BasePermission):
    """Any authenticated member can create a donation (self-report) and
    view their own. Church-wide finance roles see everything. An HBC's
    own leader/treasurer can additionally see donations tagged to their
    group (church-paybill deposits made on the group's behalf)."""

    view_all = HasPermissionCode("finance.view")
    approve = HasPermissionCode("finance.approve")

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            if obj.member_id == user.id:
                return True
            if self.view_all().has_permission(request, view):
                return True
            if obj.hbc_group_id and (
                obj.hbc_group.leader_id == user.id
                or obj.hbc_group.treasurer_id == user.id
            ):
                return True
            return False
        return self.approve().has_permission(request, view)

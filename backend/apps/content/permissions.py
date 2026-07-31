from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.accounts.permissions import HasPermissionCode
from apps.church.models import Leadership


def ReadOnlyOrPermission(code: str):
    permission_cls = HasPermissionCode(code)

    class _Permission(BasePermission):
        def has_permission(self, request, view):
            if not (request.user and request.user.is_authenticated):
                return False
            if request.method in SAFE_METHODS:
                return True
            return permission_cls().has_permission(request, view)

    return _Permission


class AboutSectionPermission(BasePermission):
    """Read open to all authenticated members. Write requires being the
    secretary of the relevant scope (or content.manage / superuser)."""

    manage_permission = HasPermissionCode("content.manage")

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.is_superuser or self.manage_permission().has_permission(request, view):
            return True
        if obj.scope == obj.Scope.BRANCH and obj.branch_id:
            return obj.branch.secretary_id == user.id
        if obj.scope == obj.Scope.HBC and obj.hbc_group_id:
            return obj.hbc_group.secretary_id == user.id
        if obj.scope == obj.Scope.DEPARTMENT and obj.department_id:
            return obj.department.secretary_id == user.id
        return False


def is_any_kind_of_leader(user) -> bool:
    if user.is_superuser:
        return True
    if Leadership.objects.filter(user=user, status="active").exists():
        return True
    if user.departments_led.exists() or user.departments_secretary_of.exists():
        return True
    if user.hbc_groups_led.exists() or user.hbc_groups_treasured.exists() or user.hbc_groups_secretary_of.exists():
        return True
    return False


class LeaderPostPermission(BasePermission):
    """Read/write both require being recognized as a leader."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and is_any_kind_of_leader(request.user)
        )

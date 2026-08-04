from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.accounts.permissions import HasPermissionCode


def ReadOnlyOrPermission(code: str):
    permission_cls = HasPermissionCode(code)

    class _Permission(BasePermission):
        def has_permission(self, request, view):
            if request.method in SAFE_METHODS:
                return True
            if not (request.user and request.user.is_authenticated):
                return False
            return permission_cls().has_permission(request, view)

    return _Permission

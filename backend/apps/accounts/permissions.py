from rest_framework.permissions import BasePermission


def HasPermissionCode(code: str):
    """
    Factory — returns a DRF permission class bound to one permission code.
    Usage in a view:
        permission_classes = [HasPermissionCode("groups.manage")]
    """

    class _HasPermissionCode(BasePermission):
        message = f"You do not have the '{code}' permission."

        def has_permission(self, request, view):
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.has_permission(code)
            )

    _HasPermissionCode.__name__ = f"HasPermission_{code.replace('.', '_')}"
    return _HasPermissionCode


class IsAuthenticatedMember(BasePermission):
    """Any signed-in user — used for the member-level write-only endpoints
    (Prayer Request, Counselling booking, Catechism registration, etc.)."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
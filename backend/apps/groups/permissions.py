from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrGroupPermission(BasePermission):
    """
    Authenticated users can read.
    Users with the 'groups.manage' permission can write.
    """

    permission_code = "groups.manage"

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        return request.user.has_permission(self.permission_code)
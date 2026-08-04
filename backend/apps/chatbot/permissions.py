from rest_framework.permissions import BasePermission


class OwnBibleChatPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id or request.user.is_superuser


class DMThreadPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        return obj.user_a_id == user_id or obj.user_b_id == user_id or request.user.is_superuser


class GroupChatPermission(BasePermission):
    """Member of the underlying department/HBC (via DepartmentMember/
    HBCMember), its leader/secretary/treasurer, or chat.message_all."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.has_permission("chat.message_all"):
            return True
        if obj.department_id:
            dept = obj.department
            if dept.leader_id == user.id or dept.secretary_id == user.id:
                return True
            return dept.memberships.filter(user=user).exists()
        if obj.hbc_group_id:
            hbc = obj.hbc_group
            if hbc.leader_id == user.id or hbc.secretary_id == user.id or hbc.treasurer_id == user.id:
                return True
            return hbc.memberships.filter(user=user).exists()
        return False

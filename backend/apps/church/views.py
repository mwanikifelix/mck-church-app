from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from rest_framework.response import Response
from apps.accounts.permissions import HasPermissionCode
from .models import Department, DepartmentMember, DepartmentPost, JoinRequest, Leadership
from .serializers import (
    DepartmentMemberSerializer,
    DepartmentPostSerializer,
    DepartmentSerializer,
    JoinRequestSerializer,
    LeadershipSerializer,
)
from .services import approve_join_request, reject_join_request
from .models import Department, Leadership
from .serializers import DepartmentSerializer, LeadershipSerializer


def ReadOnlyOrPermission(code: str):
    """GET/HEAD/OPTIONS allowed for any authenticated member (Section 2b:
    members can view departments/leadership). Write methods require the
    given permission code."""
    permission_cls = HasPermissionCode(code)

    class _Permission(BasePermission):
        def has_permission(self, request, view):
            if not (request.user and request.user.is_authenticated):
                return False
            if request.method in SAFE_METHODS:
                return True
            return permission_cls().has_permission(request, view)

    return _Permission


class DepartmentViewSet(viewsets.ModelViewSet):
    """/api/church/departments/ — list/retrieve open to all members,
    create/update/delete requires dept.manage_own (or System Admin's
    full permission set)."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [ReadOnlyOrPermission("dept.manage_own")]


class LeadershipViewSet(viewsets.ModelViewSet):
    """/api/church/leadership/ — the home-page leadership carousel
    (Section 3A). List/retrieve open to all members, writes require
    leadership.manage."""
    serializer_class = LeadershipSerializer
    permission_classes = [ReadOnlyOrPermission("leadership.manage")]

    def get_queryset(self):
        qs = Leadership.objects.all()
        if self.request.query_params.get("active_only") == "true":
            qs = qs.filter(status="active")
        return qs

class DepartmentMemberViewSet(viewsets.ModelViewSet):
    queryset = DepartmentMember.objects.select_related("department", "user")
    serializer_class = DepartmentMemberSerializer
    permission_classes = [ReadOnlyOrPermission("dept.manage_own")]
    filterset_fields = ["department"]


class JoinRequestViewSet(viewsets.ModelViewSet):
    queryset = JoinRequest.objects.select_related("department", "user")
    serializer_class = JoinRequestSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["department", "status"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        jr = self.get_object()
        dept = jr.department
        if dept.leader_id != request.user.id and dept.secretary_id != request.user.id and not request.user.is_superuser:
            return Response({"detail": "Only that department's leader or secretary can approve."}, status=403)
        approve_join_request(jr)
        return Response(self.get_serializer(jr).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        jr = self.get_object()
        dept = jr.department
        if dept.leader_id != request.user.id and dept.secretary_id != request.user.id and not request.user.is_superuser:
            return Response({"detail": "Only that department's leader or secretary can reject."}, status=403)
        reject_join_request(jr)
        return Response(self.get_serializer(jr).data)


class DepartmentPostViewSet(viewsets.ModelViewSet):
    queryset = DepartmentPost.objects.select_related("department", "author")
    serializer_class = DepartmentPostSerializer
    permission_classes = [ReadOnlyOrPermission("dept.manage_own")]
    filterset_fields = ["department"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

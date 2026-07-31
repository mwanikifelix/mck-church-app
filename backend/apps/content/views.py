from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.church.models import Department, DepartmentPost
from apps.hbc.models import HBCGroup, HBCPost

from .models import Announcement, LeaderPost, Livestream, Sermon
from .permissions import LeaderPostPermission, ReadOnlyOrPermission
from .serializers import (
    AnnouncementSerializer,
    LeaderPostSerializer,
    LivestreamSerializer,
    SermonSerializer,
)


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related("author", "branch")
    serializer_class = AnnouncementSerializer
    permission_classes = [ReadOnlyOrPermission("content.manage")]
    filterset_fields = ["branch", "is_pinned"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SermonViewSet(viewsets.ModelViewSet):
    queryset = Sermon.objects.select_related("branch")
    serializer_class = SermonSerializer
    permission_classes = [ReadOnlyOrPermission("content.manage")]
    filterset_fields = ["branch"]


class LivestreamViewSet(viewsets.ModelViewSet):
    queryset = Livestream.objects.select_related("branch")
    serializer_class = LivestreamSerializer
    permission_classes = [ReadOnlyOrPermission("content.manage")]
    filterset_fields = ["branch", "is_live"]


class LeaderPostViewSet(viewsets.ModelViewSet):
    queryset = LeaderPost.objects.select_related("author")
    serializer_class = LeaderPostSerializer
    permission_classes = [LeaderPostPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def forward(self, request, pk=None):
        """Forward this leader post into a department's or HBC's own
        feed. Requires being that specific department/HBC's leader or
        secretary (not just any leader)."""
        post = self.get_object()
        user = request.user
        dept_id = request.data.get("department")
        hbc_id = request.data.get("hbc_group")

        if not dept_id and not hbc_id:
            return Response(
                {"detail": "Provide 'department' or 'hbc_group' to forward to."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if dept_id:
            try:
                dept = Department.objects.get(pk=dept_id)
            except Department.DoesNotExist:
                return Response({"detail": "Department not found."}, status=404)
            if dept.leader_id != user.id and dept.secretary_id != user.id and not user.is_superuser:
                return Response(
                    {"detail": "Only that department's leader or secretary can forward here."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            created = DepartmentPost.objects.create(
                department=dept, author=user, title=post.title, body=post.body
            )
            return Response({"detail": "Forwarded to department.", "department_post_id": created.id}, status=201)

        try:
            hbc = HBCGroup.objects.get(pk=hbc_id)
        except HBCGroup.DoesNotExist:
            return Response({"detail": "HBC group not found."}, status=404)
        if (
            hbc.leader_id != user.id
            and hbc.treasurer_id != user.id
            and hbc.secretary_id != user.id
            and not user.is_superuser
        ):
            return Response(
                {"detail": "Only that HBC's leader, treasurer, or secretary can forward here."},
                status=status.HTTP_403_FORBIDDEN,
            )
        created = HBCPost.objects.create(
            hbc_group=hbc, author=user, title=post.title, body=post.body
        )
        return Response({"detail": "Forwarded to HBC group.", "hbc_post_id": created.id}, status=201)

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.accounts.models import User

from .models import CounsellingRequest
from .permissions import CounsellingRequestPermission
from .serializers import ClergyDirectoryEntrySerializer, CounsellingRequestSerializer


class CounsellingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = CounsellingRequestSerializer
    permission_classes = [CounsellingRequestPermission]

    def get_queryset(self):
        user = self.request.user
        qs = CounsellingRequest.objects.select_related("user", "counsellor")
        if user.is_superuser or user.has_permission("pastoral.view_all"):
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClergyDirectoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Public — auto-populated from real accounts flagged is_clergy on
    their Role, not manually curated content."""

    queryset = User.objects.filter(role__is_clergy=True, is_active=True).select_related(
        "role", "branch"
    )
    serializer_class = ClergyDirectoryEntrySerializer
    permission_classes = [AllowAny]
    filterset_fields = ["branch", "role"]

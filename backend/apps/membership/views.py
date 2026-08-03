from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import HasPermissionCode

from .models import ChurchContact, ChurchProfile, MembershipStatusChange
from .permissions import ReadOnlyOrPermission
from .serializers import (
    ChurchContactSerializer,
    ChurchProfileSerializer,
    MembershipCardSerializer,
    MembershipStatusChangeSerializer,
)


class MembershipCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        if user_id and str(user_id) != str(request.user.id):
            if not (request.user.is_superuser or request.user.has_permission("members.view_all")):
                return Response({"detail": "Not permitted to view this card."}, status=403)
            target = User.objects.filter(pk=user_id).first()
            if not target:
                return Response({"detail": "Member not found."}, status=404)
        else:
            target = request.user
        return Response(MembershipCardSerializer(target).data)


class ChurchProfileView(APIView):
    permission_classes = [ReadOnlyOrPermission("membership.manage_status")]

    def get(self, request):
        return Response(ChurchProfileSerializer(ChurchProfile.get_solo()).data)

    def put(self, request):
        profile = ChurchProfile.get_solo()
        serializer = ChurchProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChurchContactViewSet(viewsets.ModelViewSet):
    queryset = ChurchContact.objects.all()
    serializer_class = ChurchContactSerializer
    permission_classes = [ReadOnlyOrPermission("membership.manage_status")]


class MembershipStatusChangeViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipStatusChangeSerializer
    permission_classes = [IsAuthenticated, HasPermissionCode("membership.manage_status")]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return MembershipStatusChange.objects.select_related("user", "changed_by")

    def perform_create(self, serializer):
        user = serializer.validated_data["user"]
        old_status = user.status
        new_status = serializer.validated_data["new_status"]
        instance = serializer.save(old_status=old_status, changed_by=self.request.user)
        user.status = new_status
        user.save(update_fields=["status"])
        return instance

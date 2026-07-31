from django.db.models import Count, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import HBCContribution, HBCGroup, HBCMember, HBCPost
from .permissions import IsHBCGroupTreasurerLeaderOrManager
from .serializers import (
    HBCContributionSerializer,
    HBCGroupSerializer,
    HBCMemberSerializer,
    HBCPostSerializer,
)


class HBCGroupViewSet(viewsets.ModelViewSet):
    queryset = HBCGroup.objects.select_related("branch", "leader").annotate(
        member_count=Count("memberships", distinct=True),
        total_contributions=Sum("contributions__amount"),
    )
    serializer_class = HBCGroupSerializer
    permission_classes = [IsHBCGroupTreasurerLeaderOrManager]
    filterset_fields = ["branch", "leader", "is_active"]
    search_fields = ["name", "location"]

    @action(detail=False, methods=["get"])
    def mine(self, request):
        membership = HBCMember.objects.filter(user=request.user).select_related("hbc_group").first()
        if not membership:
            return Response({"detail": "Not in an HBC group."}, status=404)
        group = self.get_queryset().get(pk=membership.hbc_group_id)
        return Response(self.get_serializer(group).data)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        group = self.get_object()
        membership, created = HBCMember.objects.get_or_create(hbc_group=group, user=request.user)
        return Response(
            HBCMemberSerializer(membership).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get", "post"])
    def contributions(self, request, pk=None):
        group = self.get_object()
        if request.method == "POST":
            serializer = HBCContributionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(hbc_group=group, recorded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        qs = HBCContribution.objects.filter(hbc_group=group)
        return Response(HBCContributionSerializer(qs, many=True).data)

    @action(detail=True, methods=["get", "post"])
    def posts(self, request, pk=None):
        group = self.get_object()
        if request.method == "POST":
            serializer = HBCPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(hbc_group=group, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        qs = HBCPost.objects.filter(hbc_group=group)
        return Response(HBCPostSerializer(qs, many=True).data)

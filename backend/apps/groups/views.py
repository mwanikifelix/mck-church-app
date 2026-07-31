from django.db.models import Count

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Group,
    GroupStage,
    GroupMembership,
    GroupGraduation,
)

from .serializers import (
    GroupSerializer,
    GroupStageSerializer,
    GroupMembershipSerializer,
    GroupGraduationSerializer,
)

from .permissions import ReadOnlyOrGroupPermission


class GroupViewSet(viewsets.ModelViewSet):
    queryset = (
        Group.objects.select_related(
            "branch",
            "leader",
            "parent_group",
            "graduates_to",
        )
        .prefetch_related("stages")
        .annotate(member_total=Count("memberships"))
    )

    serializer_class = GroupSerializer
    permission_classes = [
        ReadOnlyOrGroupPermission
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    filterset_fields = [
        "branch",
        "leader",
        "is_active",
        "has_stages",
    ]

    @action(
        detail=True,
        methods=["get"],
    )
    def members(self, request, pk=None):
        group = self.get_object()

        memberships = (
            GroupMembership.objects
            .filter(group=group)
            .select_related(
                "user",
                "current_stage",
            )
        )

        serializer = GroupMembershipSerializer(
            memberships,
            many=True,
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
    )
    def join(self, request, pk=None):
        group = self.get_object()
        user = request.user

        if GroupMembership.objects.filter(
            group=group,
            user=user,
        ).exists():
            return Response(
                {
                    "detail": "You are already a member of this group."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if group.enforce_eligibility:

            if (
                user.age is not None
                and user.age < group.min_age
            ):
                return Response(
                    {
                        "detail": f"Minimum age is {group.min_age}."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if (
                user.age is not None
                and user.age > group.max_age
            ):
                return Response(
                    {
                        "detail": f"Maximum age is {group.max_age}."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if (
                group.marital_status_requirement != "any"
                and user.marital_status != group.marital_status_requirement
            ):
                return Response(
                    {
                        "detail": "You do not meet the marital status requirement."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        membership = GroupMembership.objects.create(
            group=group,
            user=user,
            status="active",
        )

        serializer = GroupMembershipSerializer(membership)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class GroupStageViewSet(viewsets.ModelViewSet):
    queryset = GroupStage.objects.select_related(
        "group",
    )

    serializer_class = GroupStageSerializer

    permission_classes = [
        ReadOnlyOrGroupPermission
    ]

    filterset_fields = [
        "group",
    ]

    ordering_fields = [
        "order",
    ]


class GroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = (
        GroupMembership.objects
        .select_related(
            "group",
            "user",
            "current_stage",
        )
    )

    serializer_class = GroupMembershipSerializer

    permission_classes = [
        ReadOnlyOrGroupPermission
    ]

    filterset_fields = [
        "group",
        "status",
    ]


class GroupGraduationViewSet(viewsets.ModelViewSet):
    queryset = (
        GroupGraduation.objects
        .select_related(
            "user",
            "from_group",
            "to_group",
            "approved_by",
        )
    )

    serializer_class = GroupGraduationSerializer

    permission_classes = [
        ReadOnlyOrGroupPermission
    ]

    filterset_fields = [
        "to_group",
    ]

    @action(
        detail=False,
        methods=["post"],
    )
    def graduate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        graduation = serializer.save(
            approved_by=request.user
        )

        GroupMembership.objects.filter(
            user=graduation.user,
            group=graduation.from_group,
        ).update(
            status="graduated"
        )

        GroupMembership.objects.update_or_create(
            user=graduation.user,
            group=graduation.to_group,
            defaults={
                "status": "active",
            },
        )

        return Response(
            self.get_serializer(graduation).data,
            status=status.HTTP_201_CREATED,
        )
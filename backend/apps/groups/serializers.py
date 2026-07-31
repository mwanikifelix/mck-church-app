from rest_framework import serializers

from .models import (
    Group,
    GroupStage,
    GroupMembership,
    GroupGraduation,
)


class GroupStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStage
        fields = [
            "id",
            "group",
            "name",
            "description",
            "order",
        ]


class GroupSerializer(serializers.ModelSerializer):
    stages = GroupStageSerializer(
        many=True,
        read_only=True,
    )

    member_count = serializers.SerializerMethodField()

    leader_name = serializers.CharField(
        source="leader.full_name",
        read_only=True,
        default=None,
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True,
        default=None,
    )

    parent_group_name = serializers.CharField(
        source="parent_group.name",
        read_only=True,
        default=None,
    )

    graduates_to_name = serializers.CharField(
        source="graduates_to.name",
        read_only=True,
        default=None,
    )

    class Meta:
        model = Group

        fields = [
            "id",

            "name",
            "description",
            "photo",

            "branch",
            "branch_name",

            "leader",
            "leader_name",

            "parent_group",
            "parent_group_name",

            "graduates_to",
            "graduates_to_name",

            "min_age",
            "max_age",
            "marital_status_requirement",
            "enforce_eligibility",

            "has_stages",

            "stages",

            "member_count",

            "is_active",

            "created_at",
        ]

        read_only_fields = [
            "created_at",
        ]

    def get_member_count(self, obj):
        return obj.memberships.filter(status="active").count()

    def validate(self, attrs):
        min_age = attrs.get(
            "min_age",
            getattr(self.instance, "min_age", 0),
        )

        max_age = attrs.get(
            "max_age",
            getattr(self.instance, "max_age", 120),
        )

        if min_age > max_age:
            raise serializers.ValidationError(
                {
                    "max_age": "Maximum age must be greater than or equal to minimum age."
                }
            )

        return attrs


class GroupMembershipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.full_name",
        read_only=True,
    )

    user_membership_number = serializers.CharField(
        source="user.membership_number",
        read_only=True,
        default=None,
    )

    group_name = serializers.CharField(
        source="group.name",
        read_only=True,
    )

    current_stage_name = serializers.CharField(
        source="current_stage.name",
        read_only=True,
        default=None,
    )

    class Meta:
        model = GroupMembership

        fields = [
            "id",

            "group",
            "group_name",

            "user",
            "user_name",
            "user_membership_number",

            "current_stage",
            "current_stage_name",

            "status",

            "joined_at",
        ]

        read_only_fields = [
            "joined_at",
        ]


class GroupGraduationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.full_name",
        read_only=True,
    )

    from_group_name = serializers.CharField(
        source="from_group.name",
        read_only=True,
        default=None,
    )

    to_group_name = serializers.CharField(
        source="to_group.name",
        read_only=True,
    )

    approved_by_name = serializers.CharField(
        source="approved_by.full_name",
        read_only=True,
        default=None,
    )

    class Meta:
        model = GroupGraduation

        fields = [
            "id",

            "user",
            "user_name",

            "from_group",
            "from_group_name",

            "to_group",
            "to_group_name",

            "certificate_issued",
            "certificate_reference",

            "approved_by",
            "approved_by_name",

            "notes",

            "graduated_at",
        ]

        read_only_fields = [
            "approved_by",
            "graduated_at",
        ]
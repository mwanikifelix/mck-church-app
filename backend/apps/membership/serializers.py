from rest_framework import serializers

from apps.church.models import DepartmentMember
from apps.groups.models import GroupMembership
from apps.hbc.models import HBCMember

from .models import ChurchContact, ChurchProfile, MembershipStatusChange


class ChurchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurchProfile
        fields = ["name", "motto", "vision", "mission", "email", "location"]


class ChurchContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurchContact
        fields = ["id", "title", "name", "phone", "order"]


class MembershipStatusChangeSerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(
        source="changed_by.full_name", read_only=True, default=None
    )

    class Meta:
        model = MembershipStatusChange
        fields = [
            "id", "user", "old_status", "new_status", "reason",
            "changed_by", "changed_by_name", "changed_at",
        ]
        read_only_fields = ["id", "old_status", "changed_by", "changed_at"]


class MembershipCardSerializer(serializers.Serializer):
    """Read-only aggregation — not tied to one model. Pulls together
    everything printed on the front of the card."""

    membership_number = serializers.CharField()
    full_name = serializers.CharField()
    passport_photo = serializers.ImageField()
    branch_name = serializers.SerializerMethodField()
    status = serializers.CharField()
    date_issued = serializers.DateTimeField(source="date_joined")
    department_names = serializers.SerializerMethodField()
    hbc_group_name = serializers.SerializerMethodField()
    growth_track_category = serializers.SerializerMethodField()

    def get_branch_name(self, user):
        return user.branch.name if user.branch else None

    def get_department_names(self, user):
        return list(
            DepartmentMember.objects.filter(user=user).values_list(
                "department__name", flat=True
            )
        )

    def get_hbc_group_name(self, user):
        membership = HBCMember.objects.filter(user=user).select_related("hbc_group").first()
        return membership.hbc_group.name if membership else None

    def get_growth_track_category(self, user):
        membership = (
            GroupMembership.objects.filter(user=user, status="active")
            .select_related("group")
            .first()
        )
        return membership.group.name if membership else None

from rest_framework import serializers

from .models import HBCContribution, HBCGroup, HBCMember, HBCPost


class HBCGroupSerializer(serializers.ModelSerializer):
    leader_name = serializers.CharField(source="leader.full_name", read_only=True, default=None)
    treasurer_display_name = serializers.CharField(source="treasurer.full_name", read_only=True, default=None)
    member_count = serializers.IntegerField(read_only=True, default=0)
    total_contributions = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True, default=0
    )

    class Meta:
        model = HBCGroup
        fields = [
            "id", "name", "branch", "location", "meeting_day", "meeting_time",
            "meeting_venue", "leader", "leader_name", "treasurer",
            "treasurer_display_name", "treasurer_name",
            "treasurer_phone", "subscription_fee", "subscription_type",
            "paybill_account", "member_count", "total_contributions",
            "is_active", "created_at",
        ]


class HBCMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = HBCMember
        fields = ["id", "hbc_group", "user", "user_name", "payment_status", "paid_amount", "joined_at"]


class HBCContributionSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="member.full_name", read_only=True, default=None)

    class Meta:
        model = HBCContribution
        fields = [
            "id", "hbc_group", "member", "member_name", "amount", "phone",
            "mpesa_ref", "description", "recorded_by", "created_at",
        ]
        read_only_fields = ["recorded_by", "created_at"]


class HBCPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True, default=None)

    class Meta:
        model = HBCPost
        fields = ["id", "hbc_group", "author", "author_name", "title", "body", "allow_comments", "created_at"]
        read_only_fields = ["author", "created_at"]

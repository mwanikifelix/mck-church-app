from rest_framework import serializers

from .models import Donation, Paybill


class DonationSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="member.full_name", read_only=True, default=None)
    account_code_display = serializers.CharField(source="get_account_code_display", read_only=True)
    hbc_group_name = serializers.CharField(source="hbc_group.name", read_only=True, default=None)

    class Meta:
        model = Donation
        fields = [
            "id", "member", "member_name", "account_code", "account_code_display",
            "amount", "phone", "mpesa_ref", "description", "hbc_group",
            "hbc_group_name", "recorded_by", "created_at",
        ]
        read_only_fields = ["id", "recorded_by", "created_at"]


class PaybillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paybill
        fields = ["id", "number", "is_active", "updated_at"]

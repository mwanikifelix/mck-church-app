from rest_framework import serializers

from apps.accounts.models import User

from .models import CounsellingRequest


class CounsellingRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    counsellor_name = serializers.CharField(
        source="counsellor.full_name", read_only=True, default=None
    )

    class Meta:
        model = CounsellingRequest
        fields = [
            "id", "user", "user_name", "message", "status", "requested_at",
            "confirmed_datetime", "counsellor", "counsellor_name", "admin_notes",
        ]
        read_only_fields = ["id", "user", "requested_at"]


class ClergyDirectoryEntrySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="role.name", read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True, default=None)
    branch_location = serializers.CharField(source="branch.address", read_only=True, default=None)

    class Meta:
        model = User
        fields = [
            "id", "full_name", "title", "passport_photo", "bio",
            "branch", "branch_name", "branch_location",
        ]

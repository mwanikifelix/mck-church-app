from rest_framework import serializers

from .models import PrayerRequest, PrayerSupport


class PrayerRequestSerializer(serializers.ModelSerializer):
    submitter_name = serializers.SerializerMethodField()
    support_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = PrayerRequest
        fields = [
            "id", "submitter_name", "is_anonymous", "body", "status",
            "support_count", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_submitter_name(self, obj):
        if obj.is_anonymous:
            return None
        return getattr(obj.submitter, "full_name", None)


class PrayerSupportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = PrayerSupport
        fields = ["id", "prayer_request", "user", "user_name", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

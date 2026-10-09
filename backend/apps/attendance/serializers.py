from rest_framework import serializers

from .models import AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ["id", "branch", "branch_name", "date", "checked_in_at", "distance_meters"]

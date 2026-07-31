from rest_framework import serializers

from .models import Event, EventRSVP


class EventSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True, default=None)
    hbc_group_name = serializers.CharField(source="hbc_group.name", read_only=True, default=None)
    rsvp_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "location", "start_time", "end_time",
            "branch", "department", "department_name", "hbc_group", "hbc_group_name",
            "created_by", "rsvp_count", "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class EventRSVPSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = EventRSVP
        fields = ["id", "event", "user", "user_name", "status", "responded_at"]
        read_only_fields = ["id", "user", "responded_at"]

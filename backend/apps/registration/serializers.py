from rest_framework import serializers

from .models import CatechismRegistration, RegistrationWindow


class RegistrationWindowSerializer(serializers.ModelSerializer):
    is_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = RegistrationWindow
        fields = ["id", "name", "description", "opens_at", "closes_at", "is_open"]
        read_only_fields = ["id"]


class CatechismRegistrationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    window_name = serializers.CharField(source="window.name", read_only=True)

    class Meta:
        model = CatechismRegistration
        fields = ["id", "window", "window_name", "user", "user_name", "status", "notes", "submitted_at"]
        read_only_fields = ["id", "user", "status", "submitted_at"]

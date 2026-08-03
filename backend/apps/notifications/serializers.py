from rest_framework import serializers

from .models import DailyVerse, DeviceToken, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "category", "display_style", "title", "body", "is_read", "created_at"]
        read_only_fields = ["id", "category", "display_style", "title", "body", "created_at"]


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ["id", "token", "platform", "created_at"]
        read_only_fields = ["id", "created_at"]


class DailyVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyVerse
        fields = ["id", "date", "reference", "text", "translation"]

from rest_framework import serializers

from .models import (
    BibleChatMessage,
    BibleChatSession,
    DirectMessage,
    DMThread,
    GroupChatMessage,
    GroupChatThread,
)


class BibleChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleChatMessage
        fields = ["id", "session", "is_from_bot", "content", "created_at"]
        read_only_fields = ["id", "is_from_bot", "created_at"]


class BibleChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleChatSession
        fields = ["id", "title", "created_at"]
        read_only_fields = ["id", "created_at"]


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = DirectMessage
        fields = ["id", "thread", "sender", "sender_name", "content", "is_read", "created_at"]
        read_only_fields = ["id", "sender", "is_read", "created_at"]


class DMThreadSerializer(serializers.ModelSerializer):
    other_user_name = serializers.SerializerMethodField()

    class Meta:
        model = DMThread
        fields = ["id", "user_a", "user_b", "other_user_name", "created_at"]
        read_only_fields = ["id", "user_a", "user_b", "created_at"]

    def get_other_user_name(self, obj):
        request_user = self.context["request"].user
        other = obj.user_b if obj.user_a_id == request_user.id else obj.user_a
        return other.full_name


class GroupChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = GroupChatMessage
        fields = ["id", "thread", "sender", "sender_name", "content", "created_at"]
        read_only_fields = ["id", "sender", "created_at"]


class GroupChatThreadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = GroupChatThread
        fields = ["id", "department", "hbc_group", "name", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_name(self, obj):
        if obj.department_id:
            return obj.department.name
        if obj.hbc_group_id:
            return obj.hbc_group.name
        return None

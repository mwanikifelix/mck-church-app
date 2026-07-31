from rest_framework import serializers

from .models import Announcement, LeaderPost, Livestream, Sermon


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True, default=None)

    class Meta:
        model = Announcement
        fields = ["id", "title", "body", "author", "author_name", "is_pinned", "branch", "created_at"]
        read_only_fields = ["id", "author", "created_at"]


class SermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sermon
        fields = ["id", "title", "preacher", "date", "description", "audio_url", "video_url", "thumbnail", "branch", "created_at"]
        read_only_fields = ["id", "created_at"]


class LivestreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestream
        fields = ["id", "title", "platform", "url", "scheduled_for", "is_live", "branch", "created_at"]
        read_only_fields = ["id", "created_at"]


class LeaderPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True, default=None)

    class Meta:
        model = LeaderPost
        fields = ["id", "title", "body", "author", "author_name", "created_at"]
        read_only_fields = ["id", "author", "created_at"]

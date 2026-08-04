from rest_framework import serializers

from .models import Department, DepartmentMember, DepartmentPost, JoinRequest, Leadership


class DepartmentSerializer(serializers.ModelSerializer):
    leader_name = serializers.CharField(source="leader.full_name", read_only=True, default=None)

    class Meta:
        model = Department
        fields = [
            "id", "name", "description", "photo",
            "branch", "leader", "leader_name", "meeting_day", "meeting_time", "created_at",
        ]


class LeadershipSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True, default=None)

    class Meta:
        model = Leadership
        fields = [
            "id", "full_name", "position", "category", "photo", "bio",
            "user", "department", "department_name", "branch",
            "order", "status",
        ]

class DepartmentMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = DepartmentMember
        fields = ["id", "department", "user", "user_name", "joined_at"]
        read_only_fields = ["id", "joined_at"]


class JoinRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = JoinRequest
        fields = ["id", "department", "user", "user_name", "status", "message", "created_at", "decided_at"]
        read_only_fields = ["id", "status", "created_at", "decided_at"]


class DepartmentPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True, default=None)

    class Meta:
        model = DepartmentPost
        fields = ["id", "department", "author", "author_name", "title", "body", "created_at"]
        read_only_fields = ["id", "author", "created_at"]

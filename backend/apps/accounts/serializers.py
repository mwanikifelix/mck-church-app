from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Branch, Permission, Role, User


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "address", "latitude", "longitude", "attendance_radius_meters"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "description"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="code"
    )

    class Meta:
        model = Role
        fields = ["id", "name", "is_admin", "can_act_as_superintendent", "permissions"]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email", "full_name", "passport_photo",
            "password", "confirm_password", "branch",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        source="branch", queryset=Branch.objects.all(), write_only=True, required=False
    )
    role = RoleSerializer(read_only=True)
    age = serializers.ReadOnlyField()
    visible_folders = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "passport_photo", "membership_number",
            "branch", "branch_id", "role", "date_of_birth", "marital_status",
            "status", "age", "visible_folders", "date_joined",
        ]
        read_only_fields = ["id", "email", "membership_number", "role", "date_joined"]


class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()
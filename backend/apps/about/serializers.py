from rest_framework import serializers

from .models import Facility, GalleryPhoto, ServiceSchedule


class GalleryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryPhoto
        fields = ["id", "image", "caption", "branch", "uploaded_by", "created_at"]
        read_only_fields = ["id", "uploaded_by", "created_at"]


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["id", "name", "description", "photo", "branch"]


class ServiceScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSchedule
        fields = ["id", "name", "day", "time", "branch", "order"]

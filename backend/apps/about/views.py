from rest_framework import viewsets

from .models import Facility, GalleryPhoto, ServiceSchedule
from .permissions import ReadOnlyOrPermission
from .serializers import FacilitySerializer, GalleryPhotoSerializer, ServiceScheduleSerializer


class GalleryPhotoViewSet(viewsets.ModelViewSet):
    queryset = GalleryPhoto.objects.select_related("branch", "uploaded_by")
    serializer_class = GalleryPhotoSerializer
    permission_classes = [ReadOnlyOrPermission("ict.manage_content")]
    filterset_fields = ["branch"]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.select_related("branch")
    serializer_class = FacilitySerializer
    permission_classes = [ReadOnlyOrPermission("content.manage")]
    filterset_fields = ["branch"]


class ServiceScheduleViewSet(viewsets.ModelViewSet):
    queryset = ServiceSchedule.objects.select_related("branch")
    serializer_class = ServiceScheduleSerializer
    permission_classes = [ReadOnlyOrPermission("content.manage")]
    filterset_fields = ["branch"]

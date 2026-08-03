from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import PrayerRequest, PrayerSupport
from .permissions import PrayerRequestPermission
from .serializers import PrayerRequestSerializer, PrayerSupportSerializer


class PrayerRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PrayerRequestSerializer
    permission_classes = [PrayerRequestPermission]

    def get_queryset(self):
        user = self.request.user
        qs = PrayerRequest.objects.annotate(support_count=Count("supporters"))
        if user.is_superuser or user.has_permission("prayer.manage"):
            return qs
        return qs.filter(submitter=user)

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)

    @action(detail=True, methods=["post"])
    def support(self, request, pk=None):
        prayer_request = self.get_object()
        support, created = PrayerSupport.objects.get_or_create(
            prayer_request=prayer_request, user=request.user
        )
        return Response(
            PrayerSupportSerializer(support).data,
            status=201 if created else 200,
        )

    @action(detail=True, methods=["post"])
    def mark_answered(self, request, pk=None):
        prayer_request = self.get_object()
        prayer_request.status = PrayerRequest.Status.ANSWERED
        prayer_request.save(update_fields=["status"])
        return Response(self.get_serializer(prayer_request).data)

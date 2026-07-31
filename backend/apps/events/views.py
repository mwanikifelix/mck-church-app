from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, EventRSVP
from .permissions import ReadOnlyOrPermission
from .serializers import EventRSVPSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("branch", "department", "hbc_group").annotate(
        rsvp_count=Count("rsvps")
    )
    serializer_class = EventSerializer
    permission_classes = [ReadOnlyOrPermission("events.manage")]
    filterset_fields = ["branch", "department", "hbc_group"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def rsvp(self, request, pk=None):
        event = self.get_object()
        status_value = request.data.get("status", EventRSVP.Status.ATTENDING)
        rsvp, _ = EventRSVP.objects.update_or_create(
            event=event, user=request.user, defaults={"status": status_value}
        )
        return Response(EventRSVPSerializer(rsvp).data)

    @action(detail=True, methods=["get"])
    def attendees(self, request, pk=None):
        event = self.get_object()
        qs = EventRSVP.objects.filter(event=event).select_related("user")
        return Response(EventRSVPSerializer(qs, many=True).data)

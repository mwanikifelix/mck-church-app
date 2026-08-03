from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import User

from .models import DailyVerse, DeviceToken, Notification
from .permissions import BroadcastPermission, NotificationPermission
from .serializers import DailyVerseSerializer, DeviceTokenSerializer, NotificationSerializer
from .services import notify


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [NotificationPermission]
    http_method_names = ["get", "patch", "delete", "post", "head", "options"]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({"detail": "All marked as read."})

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated, BroadcastPermission])
    def broadcast(self, request):
        title = request.data.get("title")
        body = request.data.get("body", "")
        display_style = request.data.get("display_style", Notification.DisplayStyle.PERSISTENT)
        if not title:
            return Response({"detail": "title is required."}, status=status.HTTP_400_BAD_REQUEST)
        notify(
            User.objects.filter(is_active=True), title=title, body=body,
            display_style=display_style, sent_by=request.user,
        )
        return Response({"detail": "Broadcast sent."}, status=status.HTTP_201_CREATED)


class DeviceTokenViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeviceToken.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyVerseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyVerse.objects.all()
    serializer_class = DailyVerseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def today(self, request):
        verse = DailyVerse.objects.filter(date=timezone.localdate()).first()
        if not verse:
            return Response({"detail": "No verse set for today."}, status=404)
        return Response(self.get_serializer(verse).data)

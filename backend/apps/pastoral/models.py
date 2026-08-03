import uuid

from django.conf import settings
from django.db import models


class CounsellingRequest(models.Model):
    """Open request flow, not fixed time slots — member submits a
    reason/message with no time picked; a counsellor reviews, confirms,
    and allocates a specific date/time. Confidential like PrayerRequest:
    only the requester and pastoral.view_all holders can see it."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="counselling_requests"
    )
    message = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    confirmed_datetime = models.DateTimeField(null=True, blank=True)
    counsellor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="counselling_assignments",
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"Counselling request from {self.user} ({self.status})"

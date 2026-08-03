import uuid

from django.conf import settings
from django.db import models


class PrayerRequest(models.Model):
    """Confidential by default — visible only to the submitter and
    anyone holding prayer.manage. is_anonymous hides the submitter's
    identity in output; the FK is always kept so the submitter can
    still view their own request."""

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        ANSWERED = "answered", "Answered"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="prayer_requests",
    )
    is_anonymous = models.BooleanField(default=False)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Prayer request ({self.status})"


class PrayerSupport(models.Model):
    """Tracks who is 'praying for this' — only meaningful for people who
    already have visibility into the request (submitter or prayer.manage)."""

    prayer_request = models.ForeignKey(
        PrayerRequest, on_delete=models.CASCADE, related_name="supporters"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prayer_supports"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("prayer_request", "user")

    def __str__(self):
        return f"{self.user} praying for {self.prayer_request_id}"

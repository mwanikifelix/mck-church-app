import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class RegistrationWindow(models.Model):
    """Generic open/close period — reusable for Catechism today, and
    later for other things (event RSVP cutoffs, HBC/department join
    periods) by giving them their own FK to this model."""

    name = models.CharField(max_length=150)  # "Catechism 2026 Term 1"
    description = models.TextField(blank=True)
    opens_at = models.DateTimeField()
    closes_at = models.DateTimeField()

    class Meta:
        ordering = ["-opens_at"]

    def __str__(self):
        return self.name

    @property
    def is_open(self) -> bool:
        now = timezone.now()
        return self.opens_at <= now <= self.closes_at


class CatechismRegistration(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    window = models.ForeignKey(
        RegistrationWindow, on_delete=models.CASCADE, related_name="catechism_registrations"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="catechism_registrations"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("window", "user")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.user} - {self.window} ({self.status})"

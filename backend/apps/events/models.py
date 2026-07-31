import uuid

from django.conf import settings
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="events", null=True, blank=True,
        help_text="Null = church-wide event.",
    )
    department = models.ForeignKey(
        "church.Department", on_delete=models.CASCADE,
        related_name="events", null=True, blank=True,
    )
    hbc_group = models.ForeignKey(
        "hbc.HBCGroup", on_delete=models.CASCADE,
        related_name="events", null=True, blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.title} ({self.start_time.date()})"


class EventRSVP(models.Model):
    class Status(models.TextChoices):
        ATTENDING = "attending", "Attending"
        MAYBE = "maybe", "Maybe"
        NOT_ATTENDING = "not_attending", "Not Attending"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_rsvps"
    )
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ATTENDING)
    responded_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user} -> {self.event} ({self.status})"

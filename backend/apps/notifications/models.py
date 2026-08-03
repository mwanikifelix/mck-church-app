import uuid

from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Category(models.TextChoices):
        GENERAL = "general", "General"
        DEPARTMENT = "department", "Department"
        HBC = "hbc", "HBC"
        GIVING = "giving", "Giving"
        EVENT = "event", "Event"
        PRAYER = "prayer", "Prayer"
        DAILY_VERSE = "daily_verse", "Daily Verse"

    class DisplayStyle(models.TextChoices):
        TOAST = "toast", "Toast (pops up, auto-dismisses)"
        PERSISTENT = "persistent", "Persistent (stays in notification list)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    display_style = models.CharField(
        max_length=10, choices=DisplayStyle.choices, default=DisplayStyle.PERSISTENT
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="notifications_sent",
        help_text="Null = system-generated.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} -> {self.recipient}"


class DeviceToken(models.Model):
    class Platform(models.TextChoices):
        ANDROID = "android", "Android"
        IOS = "ios", "iOS"
        WEB = "web", "Web"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_tokens"
    )
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=10, choices=Platform.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.platform}"


class DailyVerse(models.Model):
    """One verse per calendar date. The app fetches 'today's verse' by
    querying date=today — matches the observeTodayVerse() pattern from
    the original reference design."""

    date = models.DateField(unique=True)
    reference = models.CharField(max_length=50)  # "John 3:16"
    text = models.TextField()
    translation = models.CharField(max_length=20, default="KJV")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.reference} ({self.date})"

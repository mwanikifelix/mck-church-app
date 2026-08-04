import uuid

from django.conf import settings
from django.db import models


class MembershipStatusChange(models.Model):
    """Audit trail every time a member's status changes. User.status
    always holds the current value; this table is the history."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="status_changes"
    )
    old_status = models.CharField(max_length=15, blank=True)
    new_status = models.CharField(max_length=15)
    reason = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="status_changes_made",
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.user}: {self.old_status} -> {self.new_status}"


class ChurchProfile(models.Model):
    """Singleton — static info printed on the back of the membership
    card. Only one row should ever exist."""

    name = models.CharField(max_length=150, default="MCK Wesley Church")
    logo = models.ImageField(upload_to="church_profile/", null=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    theme_title = models.CharField(max_length=200, blank=True)
    theme_scripture_text = models.TextField(blank=True)
    theme_scripture_reference = models.CharField(max_length=50, blank=True)
    motto = models.CharField(max_length=255, blank=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class ChurchContact(models.Model):
    """One 'contact person' line for the back of the card (e.g. Pastor,
    Secretary, ICT support)."""

    title = models.CharField(max_length=100)  # "Pastor", "Secretary"
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title}: {self.name}"

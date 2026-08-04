import uuid

from django.conf import settings
from django.db import models


class GalleryPhoto(models.Model):
    """Uploaded by ICT leaders only (ict.manage_content permission)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=200, blank=True)
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="gallery_photos", null=True, blank=True,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption or f"Photo {self.id}"


class Facility(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="facilities/", null=True, blank=True)
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="facilities", null=True, blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceSchedule(models.Model):
    """A row in the service-times table — 'Sunday 1st Service, 8:00AM'."""

    name = models.CharField(max_length=150)  # "1st Service", "Youth Service"
    day = models.CharField(max_length=50)  # "Sunday", "Every 1st Sunday"
    time = models.CharField(max_length=50)  # "8:00AM"
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="service_schedules", null=True, blank=True,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} - {self.day} {self.time}"

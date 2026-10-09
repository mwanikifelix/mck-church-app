import uuid

from django.conf import settings
from django.db import models


class AttendanceRecord(models.Model):
    """One check-in per member, per branch, per day. Created only when
    the member is physically within the branch's attendance radius."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance_records"
    )
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE, related_name="attendance_records"
    )
    date = models.DateField()
    checked_in_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance_meters = models.FloatField()

    class Meta:
        unique_together = ("user", "branch", "date")
        ordering = ["-checked_in_at"]

    def __str__(self):
        return f"{self.user} @ {self.branch} on {self.date}"

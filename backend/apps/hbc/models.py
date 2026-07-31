import uuid

from django.conf import settings
from django.db import models


class HBCGroup(models.Model):
    """A Home-Based Church cell — geography-based, distinct from
    church.Department (function-based) and groups.Group (growth-track)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)  # "HBC 12 — Ganjoni"
    branch = models.ForeignKey(
        "accounts.Branch",
        on_delete=models.CASCADE,
        related_name="hbc_groups",
        null=True,
        blank=True,
    )

    location = models.CharField(max_length=150, blank=True)
    meeting_day = models.CharField(max_length=20, blank=True)
    meeting_time = models.CharField(max_length=20, blank=True)
    meeting_venue = models.CharField(max_length=150, blank=True)

    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hbc_groups_led",
    )
    treasurer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hbc_groups_treasured",
        help_text="The user allowed to edit this group's paybill/treasurer info.",
    )
    treasurer_name = models.CharField(max_length=150, blank=True)
    treasurer_phone = models.CharField(max_length=20, blank=True)
    secretary = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="hbc_groups_secretary_of",
        help_text="Can edit this HBC's About section.",
    )

    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subscription_type = models.CharField(max_length=20, default="monthly")
    paybill_account = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class HBCMember(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hbc_group = models.ForeignKey(HBCGroup, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hbc_memberships"
    )
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("hbc_group", "user")

    def __str__(self):
        return f"{self.user} in {self.hbc_group}"


class HBCContribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hbc_group = models.ForeignKey(HBCGroup, on_delete=models.CASCADE, related_name="contributions")
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="hbc_contributions",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20, blank=True)
    mpesa_ref = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="hbc_contributions_recorded",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.amount} from {self.member} to {self.hbc_group}"


class HBCPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hbc_group = models.ForeignKey(HBCGroup, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    allow_comments = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

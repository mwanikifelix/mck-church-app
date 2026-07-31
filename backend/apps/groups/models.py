import uuid

from django.conf import settings
from django.db import models


class Group(models.Model):
    """
    Church ministry / discipleship group.
    """

    MARITAL_STATUS_CHOICES = (
        ("any", "Any"),
        ("single", "Single"),
        ("married", "Married"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    branch = models.ForeignKey(
        "accounts.Branch",
        on_delete=models.CASCADE,
        related_name="groups",
    )

    parent_group = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="groups_led",
    )

    graduates_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="graduated_from",
    )

    min_age = models.PositiveIntegerField(default=0)
    max_age = models.PositiveIntegerField(default=120)

    marital_status_requirement = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        default="any",
    )

    enforce_eligibility = models.BooleanField(default=False)

    has_stages = models.BooleanField(default=False)

    photo = models.ImageField(
        upload_to="groups/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GroupStage(models.Model):
    """
    Discipleship stages within a group.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="stages",
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("group", "order")

    def __str__(self):
        return f"{self.group.name} - {self.name}"


class GroupMembership(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("graduated", "Graduated"),
        ("removed", "Removed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_memberships",
    )

    current_stage = models.ForeignKey(
        GroupStage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "user")

    def __str__(self):
        return f"{self.user} - {self.group}"


class GroupGraduation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_graduations",
    )

    from_group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="graduations_from",
    )

    to_group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="graduations_to",
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_group_graduations",
    )

    certificate_issued = models.BooleanField(default=False)

    certificate_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    notes = models.TextField(blank=True)

    graduated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-graduated_at"]

    def __str__(self):
        return f"{self.user} → {self.to_group}"
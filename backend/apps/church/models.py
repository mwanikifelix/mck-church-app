import uuid

from django.conf import settings
from django.db import models


class Department(models.Model):
    """A ministry team — ICT, Praise & Worship, etc. Distinct from Branch
    (a physical location) — a Department can be branch-specific or
    church-wide (branch=null)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="departments/", null=True, blank=True)

    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="departments", null=True, blank=True,
        help_text="Null = church-wide department.",
    )
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="departments_led",
    )
    secretary = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="departments_secretary_of",
        help_text="Can edit this department's About section.",
    )
    meeting_day = models.CharField(max_length=20, blank=True)
    meeting_time = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LeadershipCategory(models.TextChoices):
    PASTORAL = "pastoral", "Pastoral"
    DEPARTMENT = "department", "Department"
    ADMINISTRATIVE = "administrative", "Administrative"


class Leadership(models.Model):
    """One card in the home-page leadership carousel (Section 3A).
    Deliberately separate from Department — not every leadership entry
    (e.g. the Pastor) is tied to a department, and not every department
    needs a carousel card. Field names match the church_leadership table
    from the v1.0 documentation (full_name, position, category, order,
    status) — see Reconciliation Notes Section 12."""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=120, help_text="e.g. 'Pastor', 'ICT Department Lead'")
    category = models.CharField(max_length=20, choices=LeadershipCategory.choices)
    photo = models.ImageField(upload_to="leadership/", null=True, blank=True)
    bio = models.TextField(blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="leadership_entries",
        help_text="Optional link to their actual account.",
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="leadership_entries",
    )
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="leadership_entries", null=True, blank=True,
        help_text="Null = church-wide leadership entry.",
    )

    order = models.PositiveIntegerField(default=0, help_text="Carousel display order.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "full_name"]

    def __str__(self):
        return f"{self.full_name} — {self.position}"

class DepartmentMember(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="department_memberships",
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("department", "user")

    def __str__(self):
        return f"{self.user} in {self.department}"


class JoinRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="join_requests"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="department_join_requests",
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.department} ({self.status})"


class DepartmentPost(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

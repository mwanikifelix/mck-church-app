import uuid

from django.conf import settings
from django.db import models


class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_pinned = models.BooleanField(default=False)
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="announcements", null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title


class Sermon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=150, blank=True)
    date = models.DateField()
    description = models.TextField(blank=True)
    audio_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to="sermons/", null=True, blank=True)
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="sermons", null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title} ({self.date})"


class Livestream(models.Model):
    class Platform(models.TextChoices):
        YOUTUBE = "youtube", "YouTube"
        FACEBOOK = "facebook", "Facebook"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=Platform.choices, default=Platform.YOUTUBE)
    url = models.URLField()
    scheduled_for = models.DateTimeField(null=True, blank=True)
    is_live = models.BooleanField(default=False)
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="livestreams", null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scheduled_for", "-created_at"]

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    """A piece of 'about us' content, scoped to one of four levels.
    Exactly one of branch/hbc_group/department should be set, matching
    `scope` — CHURCH scope leaves all three null (church-wide)."""

    class Scope(models.TextChoices):
        CHURCH = "church", "Church-wide"
        BRANCH = "branch", "Branch"
        HBC = "hbc", "HBC Group"
        DEPARTMENT = "department", "Department"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scope = models.CharField(max_length=20, choices=Scope.choices)
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.CASCADE,
        related_name="about_sections", null=True, blank=True,
    )
    hbc_group = models.ForeignKey(
        "hbc.HBCGroup", on_delete=models.CASCADE,
        related_name="about_sections", null=True, blank=True,
    )
    department = models.ForeignKey(
        "church.Department", on_delete=models.CASCADE,
        related_name="about_sections", null=True, blank=True,
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scope"]

    def __str__(self):
        return f"{self.get_scope_display()}: {self.title}"


class LeaderPost(models.Model):
    """A leaders-only announcement feed — visible only to anyone
    recognized as a leader (Leadership entry, or leads/is secretary of
    any Branch/Department/HBCGroup), not the general membership."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

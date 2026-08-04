import uuid

from django.conf import settings
from django.db import models


class BibleChatSession(models.Model):
    """One AI-assistant conversation thread for a member — Bible
    questions, stories, general Bible-related chat with the system."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bible_chat_sessions"
    )
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Bible chat ({self.user})"


class BibleChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        BibleChatSession, on_delete=models.CASCADE, related_name="messages"
    )
    is_from_bot = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{'Bot' if self.is_from_bot else 'User'}: {self.content[:40]}"


class DMThread(models.Model):
    """Strictly 1-to-1. Only created between two users who share an
    HBC group or a Department — enforced in services.get_or_create_dm_thread,
    not just at the permission layer."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dm_threads_as_a"
    )
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dm_threads_as_b"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_a", "user_b")

    def __str__(self):
        return f"DM: {self.user_a} <-> {self.user_b}"


class DirectMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(DMThread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dms_sent"
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.content[:40]}"


class GroupChatThread(models.Model):
    """One chat per Department or HBCGroup — auto-membership derived
    from DepartmentMember/HBCMember, no separate membership table."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.OneToOneField(
        "church.Department", on_delete=models.CASCADE, related_name="group_chat",
        null=True, blank=True,
    )
    hbc_group = models.OneToOneField(
        "hbc.HBCGroup", on_delete=models.CASCADE, related_name="group_chat",
        null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Group chat: {self.department or self.hbc_group}"


class GroupChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(GroupChatThread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="group_chat_messages"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.content[:40]}"

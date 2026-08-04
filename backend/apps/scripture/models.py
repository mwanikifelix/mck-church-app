import uuid

from django.conf import settings
from django.db import models


class BibleVersion(models.Model):
    """e.g. KJV/English, NIV/English, SUV/Kiswahili. Import files are
    scoped to one version."""

    code = models.CharField(max_length=20, unique=True)  # "KJV", "NIV", "SUV"
    name = models.CharField(max_length=150)  # "King James Version"
    language = models.CharField(max_length=50)  # "English", "Kiswahili"
    is_public_domain = models.BooleanField(
        default=False,
        help_text="False = copyrighted; verse text must come from a licensed source.",
    )

    class Meta:
        ordering = ["language", "name"]

    def __str__(self):
        return f"{self.name} ({self.language})"


class BibleBook(models.Model):
    """Book structure is shared across all versions — Genesis is book
    order 1 regardless of translation."""

    class Testament(models.TextChoices):
        OLD = "old", "Old Testament"
        NEW = "new", "New Testament"

    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, blank=True)
    testament = models.CharField(max_length=5, choices=Testament.choices)
    order = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class BibleVerse(models.Model):
    version = models.ForeignKey(BibleVersion, on_delete=models.CASCADE, related_name="verses")
    book = models.ForeignKey(BibleBook, on_delete=models.CASCADE, related_name="verses")
    chapter = models.PositiveIntegerField()
    verse_number = models.PositiveIntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ("version", "book", "chapter", "verse_number")
        ordering = ["book__order", "chapter", "verse_number"]
        indexes = [models.Index(fields=["version", "book", "chapter"])]

    def __str__(self):
        return f"{self.book.name} {self.chapter}:{self.verse_number} ({self.version.code})"


class Hymn(models.Model):
    """Metadata only — the actual displayable file lives in HymnFile.
    Searchable by number or first line, like a hymnal index."""

    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    first_line = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["number"]
        unique_together = ("number", "title")

    def __str__(self):
        return f"{self.number}. {self.title}"


class HymnFile(models.Model):
    """One file per hymn — uploaded in whatever format it exists as
    (PDF, PPT, image, or plain text)."""

    class FileType(models.TextChoices):
        PDF = "pdf", "PDF"
        PPT = "ppt", "PowerPoint"
        IMAGE = "image", "Image"
        TEXT = "text", "Text"

    hymn = models.OneToOneField(Hymn, on_delete=models.CASCADE, related_name="file")
    file_type = models.CharField(max_length=10, choices=FileType.choices)
    file = models.FileField(upload_to="hymns/", null=True, blank=True)
    text_content = models.TextField(
        blank=True, help_text="Used when file_type=text instead of an uploaded file."
    )
    branch = models.ForeignKey(
        "accounts.Branch", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="hymn_files",
        help_text="Which branch's ICT team uploaded this (informational only — "
                   "not currently permission-enforced per branch).",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="hymn_files_uploaded",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hymn} ({self.file_type})"

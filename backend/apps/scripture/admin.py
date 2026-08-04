from django.contrib import admin

from .models import BibleBook, BibleVerse, BibleVersion, Hymn, HymnFile


@admin.register(BibleVersion)
class BibleVersionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "language", "is_public_domain")
    list_filter = ("language", "is_public_domain")


@admin.register(BibleBook)
class BibleBookAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "testament")
    ordering = ("order",)


@admin.register(BibleVerse)
class BibleVerseAdmin(admin.ModelAdmin):
    list_display = ("version", "book", "chapter", "verse_number")
    list_filter = ("version", "book")
    search_fields = ("text",)


@admin.register(Hymn)
class HymnAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "first_line")
    search_fields = ("title", "first_line")
    ordering = ("number",)


@admin.register(HymnFile)
class HymnFileAdmin(admin.ModelAdmin):
    list_display = ("hymn", "file_type", "branch", "uploaded_by", "updated_at")
    list_filter = ("file_type", "branch")

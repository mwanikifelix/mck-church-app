from django.contrib import admin
from django.utils.html import format_html

from .models import Facility, GalleryPhoto, ServiceSchedule


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ("caption", "branch", "uploaded_by", "created_at", "thumbnail")
    list_filter = ("branch",)
    search_fields = ("caption",)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;" />', obj.image.url)
        return "-"


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "branch")
    list_filter = ("branch",)
    search_fields = ("name",)


@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ("name", "day", "time", "branch", "order")
    list_filter = ("branch",)
    ordering = ("order",)

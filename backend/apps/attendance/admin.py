from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "branch", "date", "checked_in_at", "distance_meters")
    list_filter = ("branch", "date")
    search_fields = ("user__full_name",)

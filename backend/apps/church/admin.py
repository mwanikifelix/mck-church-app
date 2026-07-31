from django.contrib import admin

from .models import Department, Leadership


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "branch", "leader")
    search_fields = ("name",)


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "category", "order", "status", "branch")
    list_editable = ("order", "status")
    list_filter = ("category", "status", "branch")
    search_fields = ("full_name", "position")
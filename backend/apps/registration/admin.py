from django.contrib import admin

from .models import CatechismRegistration, RegistrationWindow


@admin.register(RegistrationWindow)
class RegistrationWindowAdmin(admin.ModelAdmin):
    list_display = ("name", "opens_at", "closes_at", "is_open")
    ordering = ("-opens_at",)


@admin.register(CatechismRegistration)
class CatechismRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "window", "status", "submitted_at")
    list_filter = ("status", "window")
    search_fields = ("user__full_name",)

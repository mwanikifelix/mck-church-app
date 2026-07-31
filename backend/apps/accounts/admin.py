from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Branch, Permission, Role, User


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "attendance_radius_meters")
    search_fields = ("name", "address")


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "is_admin", "can_act_as_superintendent")
    filter_horizontal = ("permissions",)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ("full_name",)
    list_display = ("email", "full_name", "membership_number", "branch", "role", "is_active")
    search_fields = ("email", "full_name", "membership_number")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": (
            "full_name", "passport_photo", "membership_number",
            "date_of_birth", "marital_status",
        )}),
        ("Church", {"fields": ("branch", "role")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions",
        )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
    )
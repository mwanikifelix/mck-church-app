from django.contrib import admin

from .models import ChurchContact, ChurchProfile, MembershipStatusChange


@admin.register(ChurchProfile)
class ChurchProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "tagline", "theme_title", "updated_at")
    # Singleton — hide the "add" button since only one row should ever exist.
    def has_add_permission(self, request):
        return not ChurchProfile.objects.exists()


@admin.register(ChurchContact)
class ChurchContactAdmin(admin.ModelAdmin):
    list_display = ("title", "name", "phone", "order")
    ordering = ("order",)


@admin.register(MembershipStatusChange)
class MembershipStatusChangeAdmin(admin.ModelAdmin):
    list_display = ("user", "old_status", "new_status", "changed_by", "changed_at")
    list_filter = ("new_status",)
    search_fields = ("user__full_name", "user__email")
    readonly_fields = ("changed_at",)

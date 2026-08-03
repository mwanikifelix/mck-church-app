from django.contrib import admin

from .models import ChurchContact, ChurchProfile, MembershipStatusChange

admin.site.register(MembershipStatusChange)
admin.site.register(ChurchProfile)
admin.site.register(ChurchContact)

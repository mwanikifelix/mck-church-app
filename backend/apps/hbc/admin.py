from django.contrib import admin

from .models import HBCContribution, HBCGroup, HBCMember, HBCPost

admin.site.register(HBCGroup)
admin.site.register(HBCMember)
admin.site.register(HBCContribution)
admin.site.register(HBCPost)

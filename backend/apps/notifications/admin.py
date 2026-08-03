from django.contrib import admin

from .models import DailyVerse, DeviceToken, Notification

admin.site.register(Notification)
admin.site.register(DeviceToken)
admin.site.register(DailyVerse)

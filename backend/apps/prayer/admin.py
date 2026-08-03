from django.contrib import admin

from .models import PrayerRequest, PrayerSupport

admin.site.register(PrayerRequest)
admin.site.register(PrayerSupport)

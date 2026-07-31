from django.contrib import admin

from .models import Donation, Paybill

admin.site.register(Donation)
admin.site.register(Paybill)

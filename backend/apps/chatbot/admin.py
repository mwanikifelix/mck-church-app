from django.contrib import admin

from .models import BibleChatMessage, BibleChatSession, DirectMessage, DMThread

admin.site.register(BibleChatSession)
admin.site.register(BibleChatMessage)
admin.site.register(DMThread)
admin.site.register(DirectMessage)

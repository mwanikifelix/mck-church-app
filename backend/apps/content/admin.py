from django.contrib import admin

from .models import AboutSection, Announcement, LeaderPost, Livestream, Sermon

admin.site.register(Announcement)
admin.site.register(Sermon)
admin.site.register(Livestream)
admin.site.register(LeaderPost)
admin.site.register(AboutSection)

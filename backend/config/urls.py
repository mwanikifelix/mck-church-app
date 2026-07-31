from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path("api/accounts/", include("apps.accounts.urls")),
    path("api/church/", include("apps.church.urls")),
    path("api/groups/", include("apps.groups.urls")),
    path("api/hbc/", include("apps.hbc.urls")),
    path("api/giving/", include("apps.giving.urls")),
    # path("api/events/", include("apps.events.urls")),
    # path("api/membership/", include("apps.membership.urls")),
    path("api/giving/", include("apps.giving.urls")),
    # path("api/pastoral/", include("apps.pastoral.urls")),
    path("api/content/", include("apps.content.urls")),
    # path("api/chatbot/", include("apps.chatbot.urls")),
    # path("api/notifications/", include("apps.notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
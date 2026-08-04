from rest_framework.routers import DefaultRouter

from .views import BibleChatSessionViewSet, DMThreadViewSet, GroupChatThreadViewSet

router = DefaultRouter()
router.register("bible-chat", BibleChatSessionViewSet, basename="bible-chat-session")
router.register("dm", DMThreadViewSet, basename="dm-thread")
router.register("group-chat", GroupChatThreadViewSet, basename="group-chat-thread")

urlpatterns = router.urls

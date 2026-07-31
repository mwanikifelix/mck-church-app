from rest_framework.routers import DefaultRouter

from .views import AnnouncementViewSet, LeaderPostViewSet, LivestreamViewSet, SermonViewSet

router = DefaultRouter()
router.register("announcements", AnnouncementViewSet, basename="announcement")
router.register("sermons", SermonViewSet, basename="sermon")
router.register("livestreams", LivestreamViewSet, basename="livestream")
router.register("leader-posts", LeaderPostViewSet, basename="leader-post")

urlpatterns = router.urls

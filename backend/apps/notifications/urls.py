from rest_framework.routers import DefaultRouter

from .views import DailyVerseViewSet, DeviceTokenViewSet, NotificationViewSet

router = DefaultRouter()
router.register("", NotificationViewSet, basename="notification")
router.register("device-tokens", DeviceTokenViewSet, basename="device-token")
router.register("daily-verse", DailyVerseViewSet, basename="daily-verse")

urlpatterns = router.urls

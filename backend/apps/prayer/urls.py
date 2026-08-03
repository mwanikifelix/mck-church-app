from rest_framework.routers import DefaultRouter

from .views import PrayerRequestViewSet

router = DefaultRouter()
router.register("", PrayerRequestViewSet, basename="prayer-request")

urlpatterns = router.urls

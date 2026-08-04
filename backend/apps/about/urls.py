from rest_framework.routers import DefaultRouter

from .views import FacilityViewSet, GalleryPhotoViewSet, ServiceScheduleViewSet

router = DefaultRouter()
router.register("gallery", GalleryPhotoViewSet, basename="gallery-photo")
router.register("facilities", FacilityViewSet, basename="facility")
router.register("service-schedule", ServiceScheduleViewSet, basename="service-schedule")

urlpatterns = router.urls

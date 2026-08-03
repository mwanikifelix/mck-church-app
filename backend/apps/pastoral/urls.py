from rest_framework.routers import DefaultRouter

from .views import ClergyDirectoryViewSet, CounsellingRequestViewSet

router = DefaultRouter()
router.register("counselling", CounsellingRequestViewSet, basename="counselling-request")
router.register("clergy", ClergyDirectoryViewSet, basename="clergy-directory")

urlpatterns = router.urls

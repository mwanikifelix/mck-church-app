from rest_framework.routers import DefaultRouter

from .views import HBCGroupViewSet

router = DefaultRouter()
router.register("", HBCGroupViewSet, basename="hbc-group")

urlpatterns = router.urls

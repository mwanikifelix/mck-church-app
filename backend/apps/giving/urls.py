from rest_framework.routers import DefaultRouter

from .views import DonationViewSet, PaybillViewSet

router = DefaultRouter()
router.register("donations", DonationViewSet, basename="donation")
router.register("paybill", PaybillViewSet, basename="paybill")

urlpatterns = router.urls

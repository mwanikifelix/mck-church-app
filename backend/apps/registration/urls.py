from rest_framework.routers import DefaultRouter

from .views import CatechismRegistrationViewSet, RegistrationWindowViewSet

router = DefaultRouter()
router.register("windows", RegistrationWindowViewSet, basename="registration-window")
router.register("catechism", CatechismRegistrationViewSet, basename="catechism-registration")

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from .views import (
    GroupViewSet,
    GroupStageViewSet,
    GroupMembershipViewSet,
    GroupGraduationViewSet,
)

app_name = "groups"

router = DefaultRouter()

router.register(
    r"groups",
    GroupViewSet,
    basename="group",
)

router.register(
    r"stages",
    GroupStageViewSet,
    basename="group-stage",
)

router.register(
    r"memberships",
    GroupMembershipViewSet,
    basename="group-membership",
)

router.register(
    r"graduations",
    GroupGraduationViewSet,
    basename="group-graduation",
)

urlpatterns = router.urls
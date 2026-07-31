from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentMemberViewSet,
    DepartmentPostViewSet,
    DepartmentViewSet,
    JoinRequestViewSet,
    LeadershipViewSet,
)

app_name = "church"

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="department")
router.register("leadership", LeadershipViewSet, basename="leadership")
router.register("department-members", DepartmentMemberViewSet, basename="department-member")
router.register("join-requests", JoinRequestViewSet, basename="join-request")
router.register("department-posts", DepartmentPostViewSet, basename="department-post")

urlpatterns = router.urls
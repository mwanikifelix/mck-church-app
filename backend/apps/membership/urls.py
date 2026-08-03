from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ChurchContactViewSet,
    ChurchProfileView,
    MembershipCardView,
    MembershipStatusChangeViewSet,
)

router = DefaultRouter()
router.register("contacts", ChurchContactViewSet, basename="church-contact")
router.register("status-changes", MembershipStatusChangeViewSet, basename="status-change")

urlpatterns = [
    path("card/", MembershipCardView.as_view(), name="membership-card-me"),
    path("card/<uuid:user_id>/", MembershipCardView.as_view(), name="membership-card"),
    path("church-profile/", ChurchProfileView.as_view(), name="church-profile"),
] + router.urls

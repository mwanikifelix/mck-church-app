from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    BranchListView,
    GoogleLoginView,
    MeView,
    MemberListView,
    PermissionListView,
    QRCodeView,
    RoleDetailView,
    RoleListView,
    RoleSetPermissionsView,
    SignupView,
)

app_name = "accounts"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),           # POST email + password
    path("login/refresh/", TokenRefreshView.as_view(), name="login-refresh"),
    path("google/", GoogleLoginView.as_view(), name="google-login"),
    path("me/", MeView.as_view(), name="me"),
    path("me/qr/", QRCodeView.as_view(), name="me-qr"),
    path("members/", MemberListView.as_view(), name="member-list"),
    path("roles/", RoleListView.as_view(), name="role-list"),
    path("roles/<uuid:pk>/", RoleDetailView.as_view(), name="role-detail"),
    path("roles/<uuid:pk>/permissions/", RoleSetPermissionsView.as_view(), name="role-set-permissions"),
    path("permissions/", PermissionListView.as_view(), name="permission-list"),
    path("branches/", BranchListView.as_view(), name="branch-list"),
]
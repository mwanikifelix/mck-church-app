from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import GoogleLoginView, MeView, QRCodeView, SignupView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),           # POST email + password
    path("login/refresh/", TokenRefreshView.as_view(), name="login-refresh"),
    path("google/", GoogleLoginView.as_view(), name="google-login"),
    path("me/", MeView.as_view(), name="me"),
    path("me/qr/", QRCodeView.as_view(), name="me-qr"),
]
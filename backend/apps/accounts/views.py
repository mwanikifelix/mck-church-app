import io

import qrcode
from django.conf import settings
from django.http import HttpResponse
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import GoogleLoginSerializer, SignupSerializer, UserSerializer


def _tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class SignupView(generics.CreateAPIView):
    """POST /api/accounts/signup/ — passport photo, full name, email,
    password + confirm, optional branch. Returns JWTs + the new profile."""
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = []  # public

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, "tokens": _tokens_for(user)},
            status=status.HTTP_201_CREATED,
            )


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/accounts/me/ — current user's profile, including
    role, permissions-derived `visible_folders`, and computed `age`."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class GoogleLoginView(APIView):
    """POST /api/accounts/google/ — { "id_token": "..." } from the
    Flutter Google Sign-In SDK. Verifies server-side, creates the user on
    first login, returns JWTs."""
    permission_classes = []  # public

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payload = google_id_token.verify_oauth2_token(
                serializer.validated_data["id_token"],
                google_requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID,
            )
        except ValueError:
            return Response({"detail": "Invalid Google token."}, status=status.HTTP_401_UNAUTHORIZED)

        google_sub = payload["sub"]
        email = payload.get("email")

        user = User.objects.filter(google_sub=google_sub).first()
        if not user:
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    "full_name": payload.get("name", email),
                    "google_sub": google_sub,
                },
            )
            if not user.google_sub:
                user.google_sub = google_sub
                user.save(update_fields=["google_sub"])

        return Response({"user": UserSerializer(user).data, "tokens": _tokens_for(user)})


class QRCodeView(APIView):
    """GET /api/accounts/me/qr/ — PNG QR code encoding this member's
    membership number, for the digital membership card (Section 3: 'Me'
    folder). Generated on the fly, not stored."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(f"MCK-MEMBER:{request.user.membership_number}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return HttpResponse(buffer.getvalue(), content_type="image/png")
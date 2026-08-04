from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CatechismRegistration, RegistrationWindow
from .permissions import ReadOnlyOrPermission
from .serializers import CatechismRegistrationSerializer, RegistrationWindowSerializer


class RegistrationWindowViewSet(viewsets.ModelViewSet):
    queryset = RegistrationWindow.objects.all()
    serializer_class = RegistrationWindowSerializer
    permission_classes = [ReadOnlyOrPermission("registration.manage")]


class CatechismRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = CatechismRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = CatechismRegistration.objects.select_related("window", "user")
        if user.is_superuser or user.has_permission("registration.manage"):
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        window = serializer.validated_data["window"]
        if not window.is_open:
            raise ValidationError({"detail": "This registration window is not currently open."})
        serializer.save(user=self.request.user)

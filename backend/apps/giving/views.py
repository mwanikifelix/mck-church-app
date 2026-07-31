from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Donation, Paybill
from .permissions import DonationPermission
from .serializers import DonationSerializer, PaybillSerializer


class DonationViewSet(viewsets.ModelViewSet):
    serializer_class = DonationSerializer
    permission_classes = [DonationPermission]
    filterset_fields = ["account_code", "hbc_group"]

    def get_queryset(self):
        user = self.request.user
        qs = Donation.objects.select_related("member", "hbc_group", "recorded_by")
        if user.is_superuser or user.has_permission("finance.view"):
            return qs
        return qs.filter(
            Q(member=user) | Q(hbc_group__leader=user) | Q(hbc_group__treasurer=user)
        )

    def perform_create(self, serializer):
        serializer.save(member=self.request.user, recorded_by=self.request.user)

    @action(detail=False, methods=["get"])
    def mine(self, request):
        qs = Donation.objects.filter(member=request.user)
        return Response(self.get_serializer(qs, many=True).data)


class PaybillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Paybill.objects.filter(is_active=True)
    serializer_class = PaybillSerializer

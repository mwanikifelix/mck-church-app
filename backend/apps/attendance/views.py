from math import asin, cos, radians, sin, sqrt

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Branch

from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer


def haversine_meters(lat1, lon1, lat2, lon2):
    r = 6371000.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * r * asin(sqrt(a))


class CheckInView(APIView):
    """POST /api/attendance/check-in/ {latitude, longitude, branch?}
    Branch defaults to the member's own branch."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            lat = float(request.data["latitude"])
            lng = float(request.data["longitude"])
        except (KeyError, TypeError, ValueError):
            return Response({"detail": "latitude and longitude are required."}, status=400)

        branch_id = request.data.get("branch")
        branch = Branch.objects.filter(pk=branch_id).first() if branch_id else request.user.branch
        if branch is None:
            return Response({"detail": "No branch selected for check-in."}, status=400)
        if branch.latitude is None or branch.longitude is None:
            return Response({"detail": "This branch has no location set yet."}, status=400)

        distance = haversine_meters(lat, lng, branch.latitude, branch.longitude)
        if distance > branch.attendance_radius_meters:
            return Response(
                {
                    "detail": (
                        f"You are about {int(distance)} m from {branch.name}. "
                        f"Move within {branch.attendance_radius_meters} m to check in."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        record, created = AttendanceRecord.objects.get_or_create(
            user=request.user,
            branch=branch,
            date=timezone.localdate(),
            defaults={"latitude": lat, "longitude": lng, "distance_meters": distance},
        )
        return Response(
            AttendanceRecordSerializer(record).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class MyAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AttendanceRecord.objects.filter(user=self.request.user).select_related("branch")

from django.urls import path

from .views import CheckInView, MyAttendanceView

urlpatterns = [
    path("check-in/", CheckInView.as_view(), name="attendance-check-in"),
    path("mine/", MyAttendanceView.as_view(), name="attendance-mine"),
]

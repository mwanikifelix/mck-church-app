from django.utils import timezone

from .models import DepartmentMember, JoinRequest


def approve_join_request(join_request: JoinRequest) -> JoinRequest:
    join_request.status = JoinRequest.Status.APPROVED
    join_request.decided_at = timezone.now()
    join_request.save(update_fields=["status", "decided_at"])
    DepartmentMember.objects.get_or_create(
        department=join_request.department, user=join_request.user
    )
    return join_request


def reject_join_request(join_request: JoinRequest) -> JoinRequest:
    join_request.status = JoinRequest.Status.REJECTED
    join_request.decided_at = timezone.now()
    join_request.save(update_fields=["status", "decided_at"])
    return join_request

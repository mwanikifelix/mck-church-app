from apps.church.models import Department, DepartmentMember
from django.db import models
from apps.hbc.models import HBCGroup, HBCMember

from .models import DMThread


def _is_leader_of_shared_group(user_a, user_b) -> bool:
    """True if user_a leads/secretaries/treasures a Department or HBC
    that user_b belongs to (or vice versa)."""
    a_dept_ids = set(DepartmentMember.objects.filter(user=user_a).values_list("department_id", flat=True))
    b_dept_ids = set(DepartmentMember.objects.filter(user=user_b).values_list("department_id", flat=True))
    if Department.objects.filter(pk__in=b_dept_ids).filter(
        models.Q(leader=user_a) | models.Q(secretary=user_a)
    ).exists():
        return True
    if Department.objects.filter(pk__in=a_dept_ids).filter(
        models.Q(leader=user_b) | models.Q(secretary=user_b)
    ).exists():
        return True

    a_hbc_ids = set(HBCMember.objects.filter(user=user_a).values_list("hbc_group_id", flat=True))
    b_hbc_ids = set(HBCMember.objects.filter(user=user_b).values_list("hbc_group_id", flat=True))
    if HBCGroup.objects.filter(pk__in=b_hbc_ids).filter(
        models.Q(leader=user_a) | models.Q(secretary=user_a) | models.Q(treasurer=user_a)
    ).exists():
        return True
    if HBCGroup.objects.filter(pk__in=a_hbc_ids).filter(
        models.Q(leader=user_b) | models.Q(secretary=user_b) | models.Q(treasurer=user_b)
    ).exists():
        return True
    return False


def shares_hbc_or_department(user_a, user_b) -> bool:
    hbc_a = set(HBCMember.objects.filter(user=user_a).values_list("hbc_group_id", flat=True))
    hbc_b = set(HBCMember.objects.filter(user=user_b).values_list("hbc_group_id", flat=True))
    if hbc_a & hbc_b:
        return True
    dept_a = set(DepartmentMember.objects.filter(user=user_a).values_list("department_id", flat=True))
    dept_b = set(DepartmentMember.objects.filter(user=user_b).values_list("department_id", flat=True))
    return bool(dept_a & dept_b)


def can_message(user_a, user_b) -> bool:
    if user_a.id == user_b.id:
        return False
    if user_a.is_superuser or user_b.is_superuser:
        return True
    if user_a.has_permission("chat.message_all") or user_b.has_permission("chat.message_all"):
        return True
    if shares_hbc_or_department(user_a, user_b):
        return True
    return _is_leader_of_shared_group(user_a, user_b)


def get_or_create_dm_thread(user_a, user_b):
    """Returns (thread, created) or (None, False) if messaging isn't
    allowed between these two users."""
    if not can_message(user_a, user_b):
        return None, False
    first, second = sorted([user_a, user_b], key=lambda u: str(u.id))
    return DMThread.objects.get_or_create(user_a=first, user_b=second)


def generate_bot_reply(user_message: str) -> str:
    """Stub — swap this out for a real LLM call later without touching
    the schema or views."""
    return (
        "Thanks for your question! Bible-assistant responses aren't "
        "connected to a live AI yet — this is a placeholder reply."
    )

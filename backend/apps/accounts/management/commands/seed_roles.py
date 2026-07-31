from django.core.management.base import BaseCommand

from apps.accounts.models import Permission, Role

PERMISSIONS = [
    ("member.default", "Baseline member permissions (all signed-in users)"),
    ("youth.manage", "Full control of Youth section functions"),
    ("jctm.manage", "Full control of JCTM sub-groups"),
    ("groups.manage", "Create/manage any Group, GroupStage, GroupGraduation"),
    ("finance.view", "View Giving summaries"),
    ("finance.approve", "Process/approve Giving transactions"),
    ("finance.reports", "View finance reports (Treasurer/Admin)"),
    ("hbc.manage_members", "Full control of HBC functions"),
    ("ict.manage_content", "Full control of ICT/technical/content functions"),
    ("dept.manage_own", "Manage own department's content/roster"),
    ("reports.view", "View cross-church reports"),
    ("content.manage", "Manage announcements and daily bible verse content"),
    ("members.view_all", "View the full member list (Secretary/Admin)"),
    ("sermons.manage", "Upload/manage sermons"),
    ("livestream.manage", "Manage livestream schedule and status"),
    ("counseling.view", "View counseling/guidance bookings"),
    ("leadership.manage", "Edit church leadership carousel entries"),
]

# name -> (is_admin, can_act_as_superintendent, [permission codes])
ROLES = {
    "Member": (False, False, ["member.default"]),

    # Section 5/8a resolved: ZERO access to youth/finance/hbc/ict — not
    # view-only. This is intentionally different from "System Admin" below.
    "Superintendent Minister": (
        True, False,
        ["member.default", "reports.view", "content.manage"],
    ),
    "Pastor": (
        True, True,  # can_act_as_superintendent
        ["member.default", "reports.view", "content.manage", "counseling.view"],
    ),
    "Youth Pastor / Youth Reverend": (
        True, False,
        ["member.default", "youth.manage", "jctm.manage", "groups.manage"],
    ),
    "Youth Leader": (
        True, False,
        ["member.default", "youth.manage", "groups.manage"],
    ),
    "Finance/Giving Officer": (  # documented role name: "Treasurer"
        True, False,
        ["member.default", "finance.view", "finance.approve", "finance.reports"],
    ),
    "HBC Leader": (
        True, False,
        ["member.default", "hbc.manage_members"],
    ),
    "ICT Media": (  # renamed from "ICT Admin" to match documented role name
        True, False,
        ["member.default", "ict.manage_content", "sermons.manage", "livestream.manage"],
    ),
    "Department Leader": (  # documented role name: "Dept Admin"
        True, False,
        ["member.default", "dept.manage_own"],
    ),
    "Secretary": (
        True, False,
        ["member.default", "members.view_all", "content.manage", "leadership.manage"],
    ),

    # Documented "Admin": full access to everything. Deliberately a
    # SEPARATE role from Superintendent Minister, not a replacement for
    # it — the two represent different jobs (technical/office admin vs.
    # clergy with an intentionally restricted permission set).
    "System Admin": (
        True, False,
        [code for code, _ in PERMISSIONS],  # every permission
    ),
}


class Command(BaseCommand):
    help = "Seeds the default Permission and Role records, reconciling the granular RBAC spec with the documented role matrix."

    def handle(self, *args, **options):
        perm_objs = {}
        for code, description in PERMISSIONS:
            perm, created = Permission.objects.update_or_create(
                code=code, defaults={"description": description}
            )
            perm_objs[code] = perm
            self.stdout.write(f"  {'created' if created else 'ok'}: permission {code}")

        for name, (is_admin, can_act_as_superintendent, codes) in ROLES.items():
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "is_admin": is_admin,
                    "can_act_as_superintendent": can_act_as_superintendent,
                },
            )
            role.permissions.set([perm_objs[c] for c in codes])
            self.stdout.write(f"  {'created' if created else 'ok'}: role {name} -> {codes}")

        self.stdout.write(self.style.SUCCESS("Roles and permissions seeded."))
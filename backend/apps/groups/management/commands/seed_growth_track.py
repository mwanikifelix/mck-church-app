from django.core.management.base import BaseCommand

from apps.accounts.models import Branch
from apps.groups.models import Group, GroupStage

JCTM_STAGES = [
    ("Creche", "Toddlers with their mothers", 1),
    ("Moses 1", "Ages 2-3, below 4", 2),
    ("Moses 2", "Ages 4-6", 3),
    ("Josiah", "Ages 7-9", 4),
    ("Samuel", "Ages 10-12", 5),
    ("David", "Ages 13-15", 6),
    ("Junior Youth", "Ages 16-18", 7),
]


class Command(BaseCommand):
    help = "Seeds JCTM, Youth, and Main Church growth-track groups (with JCTM stages and graduation chain) for every branch."

    def handle(self, *args, **options):
        for branch in Branch.objects.all():
            jctm, jctm_created = Group.objects.update_or_create(
                name=f"JCTM - {branch.name}",
                defaults={
                    "branch": branch,
                    "description": "Children's ministry, ages 0-18, staged by age group.",
                    "min_age": 0,
                    "max_age": 18,
                    "marital_status_requirement": "any",
                    "enforce_eligibility": True,
                    "has_stages": True,
                },
            )
            self.stdout.write(f"  {'created' if jctm_created else 'ok'}: group {jctm.name}")

            for name, description, order in JCTM_STAGES:
                stage, stage_created = GroupStage.objects.update_or_create(
                    group=jctm, order=order,
                    defaults={"name": name, "description": description},
                )
                self.stdout.write(f"    {'created' if stage_created else 'ok'}: stage {stage.name}")

            youth, youth_created = Group.objects.update_or_create(
                name=f"Youth - {branch.name}",
                defaults={
                    "branch": branch,
                    "description": "Ages 19-35, single. Leaves on marriage or turning 36.",
                    "min_age": 19,
                    "max_age": 35,
                    "marital_status_requirement": "single",
                    "enforce_eligibility": True,
                },
            )
            self.stdout.write(f"  {'created' if youth_created else 'ok'}: group {youth.name}")

            main_church, main_created = Group.objects.update_or_create(
                name=f"Main Church - {branch.name}",
                defaults={
                    "branch": branch,
                    "description": "Everyone not currently eligible for JCTM or Youth.",
                    "min_age": 0,
                    "max_age": 120,
                    "marital_status_requirement": "any",
                    "enforce_eligibility": False,
                },
            )
            self.stdout.write(f"  {'created' if main_created else 'ok'}: group {main_church.name}")

            jctm.graduates_to = youth
            jctm.save(update_fields=["graduates_to"])
            youth.graduates_to = main_church
            youth.save(update_fields=["graduates_to"])
            self.stdout.write(f"  linked: {jctm.name} -> {youth.name} -> {main_church.name}")

        self.stdout.write(self.style.SUCCESS("Growth-track groups seeded for all branches."))

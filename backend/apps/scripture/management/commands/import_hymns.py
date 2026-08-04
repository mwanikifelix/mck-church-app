import csv

from django.core.management.base import BaseCommand

from apps.scripture.models import Hymn


class Command(BaseCommand):
    help = (
        "Import hymn metadata (number, title, first_line) from a CSV file "
        "with a header row: number,title,first_line. Actual hymn files "
        "(PDF/PPT/image/text) are uploaded separately via the API/admin."
    )

    def add_arguments(self, parser):
        parser.add_argument("file_path")

    def handle(self, *args, **options):
        created = 0
        with open(options["file_path"], newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                _, was_created = Hymn.objects.update_or_create(
                    number=int(row["number"]), title=row["title"],
                    defaults={"first_line": row.get("first_line", "")},
                )
                created += 1 if was_created else 0
        self.stdout.write(self.style.SUCCESS(f"Imported hymns ({created} new)."))

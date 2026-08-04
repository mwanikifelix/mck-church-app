import json

from django.core.management.base import BaseCommand, CommandError

from apps.scripture.models import BibleBook, BibleVerse, BibleVersion


class Command(BaseCommand):
    help = (
        "Import a Bible version from a JSON file. Expected format: a list of "
        '{"book": "John", "chapter": 3, "verse": 16, "text": "..."} objects. '
        "The BibleVersion (by --code) and every BibleBook referenced must "
        "already exist — create them via the admin first."
    )

    def add_arguments(self, parser):
        parser.add_argument("file_path")
        parser.add_argument("--code", required=True, help="BibleVersion code, e.g. KJV")

    def handle(self, *args, **options):
        try:
            version = BibleVersion.objects.get(code=options["code"])
        except BibleVersion.DoesNotExist:
            raise CommandError(f"BibleVersion with code '{options['code']}' does not exist yet.")

        with open(options["file_path"]) as f:
            data = json.load(f)

        created, skipped = 0, 0
        for entry in data:
            try:
                book = BibleBook.objects.get(name__iexact=entry["book"])
            except BibleBook.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  skip: unknown book '{entry['book']}'"))
                skipped += 1
                continue
            _, was_created = BibleVerse.objects.update_or_create(
                version=version, book=book, chapter=entry["chapter"], verse_number=entry["verse"],
                defaults={"text": entry["text"]},
            )
            created += 1 if was_created else 0

        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(data)} verses for {version.code} ({created} new, {skipped} skipped)."
        ))

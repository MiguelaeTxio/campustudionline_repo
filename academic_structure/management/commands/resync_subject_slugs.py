# /home/MiguelAeTxio/CampuStudiOnline/academic_structure/management/commands/resync_subject_slugs.py
from django.core.management.base import BaseCommand
from django.db import transaction
from academic_structure.models import Subject
from django.utils.text import slugify


class Command(BaseCommand):
    """
    Command to resynchronize the slugs of all subjects.
    This script is essential for correcting truncated or inconsistent slugs
    that may exist in the database due to past changes in the model
    or slug generation logic.
    """

    help = "Recalculates and re-saves the slug for all existing subjects."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE(
                "--- Starting slug resynchronization for Subjects ---"
            )
        )

        subjects_to_update = Subject.objects.all()
        total_subjects = subjects_to_update.count()
        updated_count = 0

        if total_subjects == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "No subjects in the database. No action required."
                )
            )
            return

        self.stdout.write(
            f"Found {total_subjects} subjects to process."
        )

        with transaction.atomic():
            for subject in subjects_to_update.iterator():
                old_slug = subject.slug

                # Force slug regeneration by emptying it
                subject.slug = ""

                # The save() method now contains the robust slug generation logic
                subject.save()

                new_slug = subject.slug

                if old_slug != new_slug:
                    updated_count += 1
                    self.stdout.write(
                        f"  -> Slug updated for '{subject.name[:50]}...': "
                        f"'{old_slug[:30]}...' -> '{new_slug[:30]}...'"
                    )

        self.stdout.write(self.style.SUCCESS("\n--- Resynchronization complete ---"))
        self.stdout.write(f"Total subjects processed: {total_subjects}")
        self.stdout.write(f"Total slugs updated: {updated_count}")
        if updated_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    "It is recommended to restart the application server to ensure all caches are invalidated."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "No slugs were found that needed updating."
                )
            )

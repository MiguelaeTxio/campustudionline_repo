# /home/MiguelAeTxio/CampuStudiOnline/academic_structure/management/commands/generate_slugs.py
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from academic_structure.models import University, Branch, Degree
import logging


class Command(BaseCommand):
    help = "Finds existing academic models (University, Branch, Degree) without a slug and generates one for them by calling their save() method."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "--- Starting slug generation process for existing data ---"
            )
        )
        logger = logging.getLogger(__name__)

        # Generate slugs for existing Universities
        self.stdout.write(self.style.NOTICE("\n1. Processing Universities..."))
        universities_to_update = University.objects.filter(
            Q(slug__isnull=True) | Q(slug="")
        )
        count = universities_to_update.count()
        if count == 0:
            self.stdout.write("All Universities already have a slug.")
        else:
            self.stdout.write(f"Found {count} Universities without a slug. Generating...")
            for i, uni in enumerate(universities_to_update, 1):
                try:
                    uni.save()  # Calls save() which generates the slug
                    self.stdout.write(
                        f"  [{i}/{count}] Slug generated for University '{uni.name}': {uni.slug}"
                    )
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"ERROR saving University {uni.pk}: {e}")
                    )

        # Generate slugs for existing Branches
        self.stdout.write(self.style.NOTICE("\n2. Processing Branches..."))
        branches_to_update = Branch.objects.filter(Q(slug__isnull=True) | Q(slug=""))
        count = branches_to_update.count()
        if count == 0:
            self.stdout.write("All Branches already have a slug.")
        else:
            self.stdout.write(f"Found {count} Branches without a slug. Generating...")
            for i, branch in enumerate(branches_to_update, 1):
                try:
                    # Ensure the parent has a slug before saving
                    if not branch.university.slug:
                        self.stdout.write(
                            f"    -> Regenerating slug for parent University '{branch.university.name}' first..."
                        )
                        branch.university.save()
                    branch.save()  # Calls save() which generates the slug
                    self.stdout.write(
                        f"  [{i}/{count}] Slug generated for Branch '{branch.name}': {branch.slug}"
                    )
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"ERROR saving Branch {branch.pk}: {e}")
                    )

        # Generate slugs for existing Degrees
        self.stdout.write(self.style.NOTICE("\n3. Processing Degrees..."))
        degrees_to_update = Degree.objects.filter(Q(slug__isnull=True) | Q(slug=""))
        count = degrees_to_update.count()
        if count == 0:
            self.stdout.write("All Degrees already have a slug.")
        else:
            self.stdout.write(f"Found {count} Degrees without a slug. Generating...")
            for i, degree in enumerate(degrees_to_update, 1):
                try:
                    # Ensure ancestors have slugs
                    if not degree.branch.university.slug:
                        self.stdout.write(
                            f"    -> Regenerating slug for parent University '{degree.branch.university.name}'..."
                        )
                        degree.branch.university.save()
                    if not degree.branch.slug:
                        self.stdout.write(
                            f"    -> Regenerating slug for parent Branch '{degree.branch.name}'..."
                        )
                        degree.branch.save()
                    degree.save()  # Calls save() which generates the slug
                    self.stdout.write(
                        f"  [{i}/{count}] Slug generated for Degree '{degree.name}': {degree.slug}"
                    )
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"ERROR saving Degree {degree.pk}: {e}")
                    )

        self.stdout.write(
            self.style.SUCCESS("\n--- Slug generation process completed. ---")
        )

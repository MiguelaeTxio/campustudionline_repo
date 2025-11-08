import json
import re
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from academic_structure.models import University, Branch, Degree, Subject, AcademicYear
from content_automation.models import PendingContentTask


class Command(BaseCommand):
    """
    Management command to import UGR data from ugr_data.json.
    Populates University, Branch, Degree, and Subject models.
    """

    help = "Imports University of Granada data from ugr_data_cleaned.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--purge",
            action="store_true",
            help="Deletes ALL existing academic data (Universities, Branches, Degrees, Subjects) before import. USE WITH CAUTION!",
        )

    def handle(self, *args, **options):
        if options["purge"]:
            self.stdout.write(
                self.style.WARNING(
                    "--purge option detected. Purging all academic directory data..."
                )
            )
            # Thanks to on_delete=CASCADE, deleting universities will wipe everything else.
            self.stdout.write(self.style.WARNING("-> Purging all pending content tasks to avoid constraint violations..."))
            PendingContentTask.objects.all().delete()
            # NOTE: This will also delete any associated ContentMaterial.
            deleted_count, _ = University.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"-> Purge complete. Deleted {deleted_count} universities and all their associated data in cascade."
                )
            )

        json_file_path = "data/ugr_data_cleaned.json"

        self.stdout.write(
            self.style.NOTICE(
                f"--- Starting UGR import from: {json_file_path} ---"
            )
        )

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise CommandError(
                f"File '{json_file_path}' not found. "
                "Make sure you have run the 'ugr_scraper.py' script first."
            )
        except json.JSONDecodeError:
            raise CommandError(
                "Error decoding JSON file. Please check its format."
            )
        except Exception as e:
            raise CommandError(f"Could not read the file: {e}")

        # Counters
        universities_created, universities_updated = 0, 0
        branches_created, branches_updated = 0, 0
        degrees_created, degrees_updated = 0, 0
        subjects_created, subjects_updated = 0, 0

        # Subject type mapping
        subject_type_map = {
            "troncal": Subject.SubjectType.CORE,
            "obligatoria": Subject.SubjectType.MANDATORY,
            "optativa": Subject.SubjectType.OPTIONAL,
            "formación básica": Subject.SubjectType.BASIC,
        }

        try:
            with transaction.atomic():
                self.stdout.write(self.style.NOTICE("\n[1/4] Syncing University..."))
                uni_obj, created = University.objects.update_or_create(
                    code=data.get("university_code", "GR"),
                    defaults={
                        "name": data.get("university_name"),
                        "url": data.get("portal_url"),
                    },
                )
                if created:
                    universities_created += 1
                else:
                    universities_updated += 1
                self.stdout.write(f" -> University '{uni_obj.name}' synced.")

                self.stdout.write(
                    self.style.NOTICE(
                        "\n[2/4, 3/4, 4/4] Syncing Branches, Degrees, and Subjects..."
                    )
                )
                degrees_data = data.get("degrees", [])
                total_degrees = len(degrees_data)

                for index, degree_data in enumerate(degrees_data):
                    branch_name = degree_data.get("branch")
                    degree_name = degree_data.get("degree_name")

                    if not branch_name or not degree_name:
                        self.stdout.write(
                            self.style.WARNING(
                                f"    -> Skipping degree due to missing branch or degree name."
                            )
                        )
                        continue

                    degree_code = (
                        f"UGR-{re.sub(r'[^A-Z0-9]', '', degree_name.upper())[:15]}"
                    )

                    self.stdout.write(
                        f"  ({index+1}/{total_degrees}) Processing Degree: {degree_name} [Branch: {branch_name}]"
                    )

                    branch_obj, created = Branch.objects.get_or_create(
                        university=uni_obj,
                        name=branch_name.strip(),
                    )
                    if created:
                        branches_created += 1
                    else:
                        branches_updated += 1

                    degree_obj, created = Degree.objects.update_or_create(
                        branch=branch_obj,
                        name=degree_name,
                        defaults={
                            "code": degree_code,
                            "degree_type": Degree.DegreeType.BACHELOR,
                            "url": degree_data.get("degree_url"),
                        },
                    )
                    if created:
                        degrees_created += 1
                    else:
                        degrees_updated += 1

                    subjects_data = degree_data.get("subjects", [])
                    for subject_data in subjects_data:
                        subject_name = subject_data.get("name")
                        subject_type_str = subject_data.get("type", "other").lower()
                        subject_year = subject_data.get("year")
                        subject_semester = subject_data.get("semester", 0)

                        subject_type_code = subject_type_map.get(
                            subject_type_str, Subject.SubjectType.OTHER
                        )

                        if not all([subject_name, subject_year is not None]):
                            self.stdout.write(
                                self.style.WARNING(
                                    f"    -> Skipping subject due to incomplete data: {subject_data}"
                                )
                            )
                            continue
                        
                        # --- INICIO REFACTORIZACIÓN ---
                        # 1. Obtener o crear el AcademicYear correspondiente.
                        academic_year_obj, _ = AcademicYear.objects.get_or_create(
                            degree=degree_obj,
                            year=subject_year
                        )
                        # --- FIN REFACTORIZACIÓN ---

                        # Prepare defaults dictionary with existing and new fields
                        defaults_dict = {
                            "subject_type": subject_type_code,
                            "learning_objectives": subject_data.get("learning_objectives", []),
                            "course_content_outline": subject_data.get("course_content_outline", []),
                            "bibliography": subject_data.get("bibliography", {}),
                        }

                        subj_obj, created = Subject.objects.update_or_create(
                            academic_year=academic_year_obj,
                            name=subject_name.strip(),
                            semester=subject_semester,
                            defaults=defaults_dict,
                        )
                        if created:
                            subjects_created += 1
                        else:
                            subjects_updated += 1

        except Exception as e:
            raise CommandError(
                f"\nError during transaction. Nothing was saved. Reason: {e}"
            )

        self.stdout.write(self.style.SUCCESS("\nUGR import completed successfully!"))
        self.stdout.write("Operation Summary:")
        self.stdout.write(
            f"  - Universities Created/Updated: {universities_created}/{universities_updated}"
        )
        self.stdout.write(
            f"  - Branches Created/Updated: {branches_created}/{branches_updated}"
        )
        self.stdout.write(
            f"  - Degrees Created/Updated: {degrees_created}/{degrees_updated}"
        )
        self.stdout.write(
            f"  - Subjects Created/Updated: {subjects_created}/{subjects_updated}"
        )

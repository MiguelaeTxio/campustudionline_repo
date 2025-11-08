from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef
from academic_structure.models import Subject, Degree, Branch, University
from contents.models import ContentMaterial

class Command(BaseCommand):
    help = 'Updates the has_public_content flag for all academic hierarchy models based on existing public ContentMaterial.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the one-time update for has_public_content flags..."))

        # Nivel 1: Actualizar Subjects
        # Un Subject tiene contenido si existe al menos un ContentMaterial público que apunte a él.
        self.stdout.write("Processing Level 1: Subjects...")
        subject_subquery = ContentMaterial.objects.filter(subjects=OuterRef('pk'), is_public=True)
        Subject.objects.update(has_public_content=Exists(subject_subquery))
        self.stdout.write(self.style.SUCCESS(f"-> Subjects updated."))

        # Nivel 2: Actualizar Degrees
        # Un Degree tiene contenido si existe al menos un Subject hijo que tenga contenido.
        self.stdout.write("Processing Level 2: Degrees...")
        degree_subquery = Subject.objects.filter(degree=OuterRef('pk'), has_public_content=True)
        Degree.objects.update(has_public_content=Exists(degree_subquery))
        self.stdout.write(self.style.SUCCESS(f"-> Degrees updated."))

        # Nivel 3: Actualizar Branches
        # Un Branch tiene contenido si existe al menos un Degree hijo que tenga contenido.
        self.stdout.write("Processing Level 3: Branches...")
        branch_subquery = Degree.objects.filter(branch=OuterRef('pk'), has_public_content=True)
        Branch.objects.update(has_public_content=Exists(branch_subquery))
        self.stdout.write(self.style.SUCCESS(f"-> Branches updated."))

        # Nivel 4: Actualizar Universities
        # Una University tiene contenido si existe al menos un Branch hijo que tenga contenido.
        self.stdout.write("Processing Level 4: Universities...")
        university_subquery = Branch.objects.filter(university=OuterRef('pk'), has_public_content=True)
        University.objects.update(has_public_content=Exists(university_subquery))
        self.stdout.write(self.style.SUCCESS(f"-> Universities updated."))

        self.stdout.write(self.style.SUCCESS("\nBackfilling process finished successfully! All has_public_content flags are now synchronized."))

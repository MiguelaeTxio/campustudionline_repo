from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject

class Command(BaseCommand):
    help = "Recalcula las banderas 'has_public_content' basándose en la arquitectura ContentHashFamily."

    def handle(self, *args, **options):
        self.stdout.write("Iniciando recálculo de visibilidad...")
        
        with transaction.atomic():
            # 1. Resetear todo a False
            self.stdout.write("- Reseteando banderas...")
            University.objects.update(has_public_content=False)
            Branch.objects.update(has_public_content=False)
            Degree.objects.update(has_public_content=False)
            AcademicYear.objects.update(has_public_content=False)
            Subject.objects.update(has_public_content=False)

            # 2. Activar Asignaturas (Nivel Base)
            # Buscamos asignaturas que tengan material público, ya sea directamente
            # o a través de su familia de contenido (arquitectura nueva).
            self.stdout.write("- Buscando contenido público...")
            
            public_subjects = Subject.objects.filter(
                Q(content_hash_family__content_material__is_public=True) | 
                Q(content_materials__is_public=True)
            ).distinct()
            
            updated_subs = public_subjects.update(has_public_content=True)
            self.stdout.write(f"  > {updated_subs} asignaturas activadas.")

            # 3. Propagación Ascendente (Bottom-Up)
            
            # Años
            years = AcademicYear.objects.filter(subjects__has_public_content=True).distinct()
            years.update(has_public_content=True)
            
            # Titulaciones
            degrees = Degree.objects.filter(academic_years__has_public_content=True).distinct()
            degrees.update(has_public_content=True)
            
            # Ramas
            branches = Branch.objects.filter(degrees__has_public_content=True).distinct()
            branches.update(has_public_content=True)
            
            # Universidades
            unis = University.objects.filter(branches__has_public_content=True).distinct()
            unis.update(has_public_content=True)

        self.stdout.write(self.style.SUCCESS("Sincronización de visibilidad completada correctamente."))

from django.core.management.base import BaseCommand
from django.db.models import Q
from academic_structure.models import Subject
import sys

class Command(BaseCommand):
    help = 'Elimina asignaturas genéricas y audita Proyectos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando proceso de purga y auditoría...'))

        # --- BLOQUES A ELIMINAR ---
        DELETE_PATTERNS = {
            'TFG/TFM': ['Trabajo Fin de', 'TFG', 'TFM', 'Trabajo de Fin de'],
            'Prácticas': ['Prácticas', 'Practicum', 'Estancias', 'Rotatorio', 'Prácticas Externas'],
            'Jornadas/Eventos': ['Jornadas', 'Seminario', 'Conferencias'],
        }

        total_deleted = 0

        for category, terms in DELETE_PATTERNS.items():
            query = Q()
            for term in terms:
                query |= Q(name__icontains=term)
            
            subjects = Subject.objects.filter(query)
            count = subjects.count()
            
            if count > 0:
                self.stdout.write(self.style.WARNING(f'\nEliminando {count} asignaturas de categoría: {category}...'))
                # Ejecutar borrado
                deleted_count, _ = subjects.delete()
                self.stdout.write(self.style.SUCCESS(f'  -> {deleted_count} eliminadas.'))
                total_deleted += deleted_count
            else:
                 self.stdout.write(f'\nCategoría {category}: No se encontraron asignaturas.')

        self.stdout.write(self.style.SUCCESS(f'\n--- TOTAL ELIMINADO: {total_deleted} ---'))

        # --- AUDITORÍA DE "PROYECTO" ---
        self.stdout.write(self.style.WARNING('\n--- AUDITORÍA DE "PROYECTO" (No se borran) ---'))
        
        project_query = Q(name__icontains='Proyecto')
        project_subjects = Subject.objects.filter(project_query).select_related('academic_year__degree__branch__university')
        project_count = project_subjects.count()

        if project_count > 0:
            self.stdout.write(f'Se encontraron {project_count} asignaturas con el término "Proyecto":')
            for s in project_subjects:
                uni_code = 'N/A'
                if s.academic_year:
                     try:
                        uni_code = s.academic_year.degree.branch.university.code
                     except AttributeError:
                        uni_code = 'ERR'
                self.stdout.write(f"  - [{uni_code}] {s.name}")
        else:
            self.stdout.write('No se encontraron asignaturas con el término "Proyecto".')


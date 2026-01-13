from django.core.management.base import BaseCommand
from django.db.models import Q
from academic_structure.models import Subject

class Command(BaseCommand):
    help = 'Elimina asignaturas tipo Proyecto fin y Proyecto exacto.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando purga selectiva de Proyectos...'))

        # Criterio 1: Contiene "proyecto fin" (ej: "Proyecto Fin de Grado")
        q_fin = Q(name__icontains='proyecto fin')
        
        # Criterio 2: Es exactamente "proyecto" (ej: "Proyecto", "PROYECTO")
        q_exact = Q(name__iexact='proyecto')

        # Combinar criterios
        query = q_fin | q_exact
        
        subjects = Subject.objects.filter(query)
        count = subjects.count()

        if count > 0:
            self.stdout.write(self.style.WARNING(f'Se encontraron {count} asignaturas para eliminar:'))
            # Listar muestra
            for s in subjects[:15]:
                self.stdout.write(f" - {s.name}")
            if count > 15:
                self.stdout.write(f" ... y {count - 15} más.")
            
            # Ejecutar borrado
            deleted, _ = subjects.delete()
            self.stdout.write(self.style.SUCCESS(f'\nELIMINADAS CON ÉXITO: {deleted} asignaturas.'))
        else:
            self.stdout.write(self.style.SUCCESS('No se encontraron asignaturas que cumplan los criterios de eliminación.'))


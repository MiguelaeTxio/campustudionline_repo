from django.core.management.base import BaseCommand
from academic_structure.models import AcademicYear

class Command(BaseCommand):
    help = 'Elimina los Años Académicos que no tienen asignaturas.'

    def handle(self, *args, **options):
        print("🧹 LIMPIEZA DE AÑOS VACÍOS")
        
        # Buscar años sin asignaturas
        empty_years = AcademicYear.objects.filter(subjects__isnull=True)
        count = empty_years.count()
        
        if count > 0:
            print(f"   found {count} años vacíos. Eliminando...")
            empty_years.delete()
            print("   ✅ Eliminados.")
        else:
            print("   ℹ️ No se encontraron años vacíos.")

from django.core.management.base import BaseCommand
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject

class Command(BaseCommand):
    help = 'Elimina datos de la UMA de forma segura (Bottom-Up)'

    def handle(self, *args, **options):
        try:
            uma = University.objects.get(code="UMA")
            self.stdout.write(self.style.WARNING(f"Iniciando purga nuclear de: {uma.name}"))

            # 1. Asignaturas
            subjs = Subject.objects.filter(academic_year__degree__branch__university=uma)
            c_sub = subjs.count()
            subjs.delete()
            self.stdout.write(f"- {c_sub} Asignaturas eliminadas.")

            # 2. Años Académicos
            years = AcademicYear.objects.filter(degree__branch__university=uma)
            c_yea = years.count()
            years.delete()
            self.stdout.write(f"- {c_yea} Años Académicos eliminados.")

            # 3. Titulaciones
            degs = Degree.objects.filter(branch__university=uma)
            c_deg = degs.count()
            degs.delete()
            self.stdout.write(f"- {c_deg} Titulaciones eliminadas.")

            # 4. Ramas
            brans = Branch.objects.filter(university=uma)
            c_bra = brans.count()
            brans.delete()
            self.stdout.write(f"- {c_bra} Ramas eliminadas.")

            # 5. Universidad
            uma.delete()
            
            self.stdout.write(self.style.SUCCESS("BASE DE DATOS LIMPIA: Rastro de la UMA erradicado."))

        except University.DoesNotExist:
            self.stdout.write(self.style.SUCCESS("La UMA ya no existe en el sistema."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error en la purga: {e}"))

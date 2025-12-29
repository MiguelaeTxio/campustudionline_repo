from django.core.management.base import BaseCommand
from django.db import transaction
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject, ContentHashFamily
# Importación segura dentro de los métodos para evitar ciclos si fuera necesario, 
# pero aquí necesitamos los modelos para los filtros.
from orchestrator.models import PendingContentTask, ContentRequest

class Command(BaseCommand):
    help = 'Elimina COMPLETAMENTE todos los datos de la Universidad de Córdoba usando borrado escalonado.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("INICIANDO PROTOCOLO DE PURGA QUIRÚRGICA (BOTTOM-UP)..."))

        target_name = "Córdoba"

        try:
            with transaction.atomic():
                # 1. Localizar la Universidad
                uni = University.objects.filter(name__icontains=target_name).first()
                
                if not uni:
                    self.stdout.write(self.style.ERROR(f"No se encontró ninguna universidad que coincida con '{target_name}'."))
                    return

                self.stdout.write(f"Objetivo localizado: {uni.name} ({uni.code})")
                self.stdout.write("NOTA: Escribe 's' y pulsa Enter para confirmar.")
                confirm = input(f"¿Estás SEGURO de que quieres eliminar {uni.name} y TODOS sus datos asociados? [s/N]: ")
                
                if confirm.lower() != 's':
                    self.stdout.write(self.style.WARNING("Operación cancelada."))
                    return

                # RECOPILACIÓN DE OBJETIVOS
                self.stdout.write("Mapeando jerarquía para borrado seguro...")
                branches = Branch.objects.filter(university=uni)
                degrees = Degree.objects.filter(branch__in=branches)
                years = AcademicYear.objects.filter(degree__in=degrees)
                subjects = Subject.objects.filter(academic_year__in=years)

                # FASE 1: Limpieza de Orquestador (Dependencias Externas)
                self.stdout.write("FASE 1: Eliminando dependencias del Orquestador...")
                
                tasks = PendingContentTask.objects.filter(subject__in=subjects)
                task_count = tasks.count()
                tasks.delete()
                self.stdout.write(f" - {task_count} Tareas pendientes eliminadas.")

                reqs = ContentRequest.objects.filter(subject__in=subjects)
                req_count = reqs.count()
                reqs.delete()
                self.stdout.write(f" - {req_count} Solicitudes de contenido eliminadas.")

                # FASE 2: Jerarquía Académica (De abajo a arriba)
                self.stdout.write("FASE 2: Eliminando Jerarquía Académica...")

                subj_count = subjects.count()
                subjects.delete()
                self.stdout.write(f" - {subj_count} Asignaturas eliminadas.")

                years_count = years.count()
                years.delete()
                self.stdout.write(f" - {years_count} Años Académicos eliminados.")

                deg_count = degrees.count()
                degrees.delete()
                self.stdout.write(f" - {deg_count} Titulaciones eliminadas.")

                branch_count = branches.count()
                branches.delete()
                self.stdout.write(f" - {branch_count} Ramas eliminadas.")

                # FASE 3: Cabecera
                self.stdout.write("FASE 3: Eliminando Universidad...")
                uni.delete()
                self.stdout.write(self.style.SUCCESS(f"¡ELIMINADO! {uni.name} ha sido purgada correctamente."))

                # FASE 4: Limpieza de Huérfanos
                self.stdout.write("FASE 4: Limpiando familias huérfanas...")
                orphans = ContentHashFamily.objects.filter(subjects__isnull=True)
                orphan_count = orphans.count()
                if orphan_count > 0:
                    orphans.delete()
                    self.stdout.write(self.style.SUCCESS(f" - {orphan_count} Familias de contenido huérfanas eliminadas."))
                else:
                    self.stdout.write(" - No se encontraron huérfanos.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"ERROR CRÍTICO DURANTE LA PURGA: {str(e)}"))

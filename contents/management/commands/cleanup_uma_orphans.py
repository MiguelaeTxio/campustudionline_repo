import sys
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db import transaction
from contents.models import ContentMaterial, ContentCopy
from orchestrator.models import PendingContentTask, ContentRequest

class Command(BaseCommand):
    help = 'Limpia contenido zombi de la UMA de forma rápida y verbosa'

    def handle(self, *args, **options):
        self.stdout.write("--- INICIANDO AUDITORÍA REAL-TIME ---")
        
        # Obtenemos materiales no libres con el conteo de asignaturas en una sola query
        materials = ContentMaterial.objects.filter(is_free_content=False).annotate(
            num_subjects=Count('subject')
        )

        to_delete_ids = []
        
        for mat in materials:
            status = ""
            is_uma = False
            
            # Verificar si pertenece a la UMA si tiene asignaturas
            if mat.num_subjects > 0:
                is_uma = mat.subject.filter(academic_year__degree__branch__university__code='UMA').exists()

            if mat.num_subjects == 0:
                status = self.style.ERROR("[ELIMINAR - HUÉRFANO]")
                to_delete_ids.append(mat.id)
            elif is_uma:
                status = self.style.ERROR("[ELIMINAR - UMA]")
                to_delete_ids.append(mat.id)
            else:
                status = self.style.SUCCESS("[CONSERVADO]")

            # Impresión inmediata (sin buffer)
            sys.stdout.write(f"{status} {mat.title[:60]}\n")
            sys.stdout.flush()

        if not to_delete_ids:
            self.stdout.write(self.style.SUCCESS("\nNo hay nada que limpiar."))
            return

        self.stdout.write(self.style.WARNING(f"\nBorrando {len(to_delete_ids)} materiales y sus dependencias..."))
        
        with transaction.atomic():
            # 1. Tareas y solicitudes
            t_count = PendingContentTask.objects.filter(subject__content_materials__id__in=to_delete_ids).delete()[0]
            r_count = ContentRequest.objects.filter(subject__content_materials__id__in=to_delete_ids).delete()[0]
            # 2. Copias
            c_count = ContentCopy.objects.filter(original_content_id__in=to_delete_ids).delete()[0]
            # 3. Material base
            m_count = ContentMaterial.objects.filter(id__in=to_delete_ids).delete()[0]

            self.stdout.write(f"   > {t_count} Tareas eliminadas.")
            self.stdout.write(f"   > {r_count} Solicitudes eliminadas.")
            self.stdout.write(f"   > {c_count} Copias eliminadas.")
            self.stdout.write(self.style.SUCCESS(f"   > {m_count} Materiales eliminados."))

        self.stdout.write(self.style.SUCCESS("\n--- LIMPIEZA FINALIZADA ---"))

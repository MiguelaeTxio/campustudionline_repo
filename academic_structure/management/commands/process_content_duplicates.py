# /home/MiguelAeTxio/CampuStudiOnline/academic_structure/management/commands/process_content_duplicates.py
from django.core.management.base import BaseCommand
from django.db.models import Count
from academic_structure.models import Subject
import time

class Command(BaseCommand):
    help = 'Procesa los content_hash duplicados, manteniendo un "maestro" y marcando el resto como NULL.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando procesamiento de content_hash duplicados..."))
        start_time = time.time()

        # 1. Encontrar los hashes que están duplicados
        duplicate_hashes_query = Subject.objects.values('content_hash') \
            .annotate(hash_count=Count('id')) \
            .filter(hash_count__gt=1, content_hash__isnull=False) \
            .order_by('-hash_count')

        total_groups = duplicate_hashes_query.count()
        if total_groups == 0:
            self.stdout.write(self.style.SUCCESS("No se encontraron grupos de contenido duplicado. Proceso finalizado."))
            return

        self.stdout.write(self.style.SUCCESS(f"Se encontraron {total_groups} grupos de contenido duplicado."))
        
        demoted_subjects_count = 0
        
        # 2. Iterar sobre cada grupo de hashes duplicados
        for group in duplicate_hashes_query:
            hash_value = group['content_hash']
            self.stdout.write(f"\n--- Procesando hash: {hash_value[:10]}... ({group['hash_count']} duplicados) ---")

            # Obtener todas las asignaturas que comparten este hash, ordenadas por fecha de creación
            subjects_with_hash = Subject.objects.filter(content_hash=hash_value).order_by('created_at', 'id')
            
            # El primero de la lista será el "maestro"
            master_subject = subjects_with_hash.first()
            self.stdout.write(self.style.SUCCESS(f"  > Maestro designado: {master_subject.id} ({master_subject.name})"))

            # El resto serán los "esclavos" a des-duplicar
            duplicates_to_demote = subjects_with_hash.exclude(pk=master_subject.pk)
            
            # 3. Actualizar los duplicados para que su hash sea NULL
            demoted_count = duplicates_to_demote.update(content_hash=None)
            
            if demoted_count > 0:
                demoted_subjects_count += demoted_count
                for demoted_subject in duplicates_to_demote:
                     self.stdout.write(self.style.WARNING(f"    > Duplicado marcado: {demoted_subject.id} ({demoted_subject.name})"))

        end_time = time.time()
        self.stdout.write(self.style.SUCCESS(
            f"\nProceso completado. Total de asignaturas marcadas como duplicadas: {demoted_subjects_count}. "
            f"Tiempo total: {end_time - start_time:.2f} segundos."
        ))



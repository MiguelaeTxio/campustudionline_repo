from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from academic_structure.models import Subject
from contents.models import ContentMaterial
import time

class Command(BaseCommand):
    help = 'Limpia ContentMaterial duplicados basándose en el content_hash de las asignaturas.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula las acciones (borrado y reasignación) sin ejecutar cambios en la base de datos.'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        mode = "[DRY RUN]" if dry_run else "[EXECUTE]"
        
        self.stdout.write(self.style.NOTICE(f"{mode} Iniciando limpieza de contenido duplicado..."))
        start_time = time.time()

        master_hashes = {
            s.content_hash: s 
            for s in Subject.objects.filter(content_hash__isnull=False)
        }
        
        candidates = Subject.objects.filter(
            Q(learning_objectives__isnull=False) | Q(course_content_outline__isnull=False) | Q(bibliography__isnull=False),
            content_hash__isnull=True
        )

        deleted_count = 0
        reassigned_count = 0
        processed_count = 0

        for duplicate_subject in candidates.iterator():
            processed_count += 1
            calculated_hash = duplicate_subject._calculate_content_hash()

            if calculated_hash in master_hashes:
                master_subject = master_hashes[calculated_hash]

                master_material = ContentMaterial.objects.filter(subjects=master_subject).first()
                duplicate_material = ContentMaterial.objects.filter(subjects=duplicate_subject).first()

                if not duplicate_material:
                    continue # No hay nada que limpiar para este duplicado

                self.stdout.write(f"\n--- Conflicto de duplicado detectado para hash {calculated_hash[:10]}... ---")
                self.stdout.write(f"  > Maestro: Subject ID {master_subject.id} ({master_subject.name})")
                self.stdout.write(f"  > Duplicado: Subject ID {duplicate_subject.id} ({duplicate_subject.name})")

                if master_material and duplicate_material:
                    self.stdout.write(self.style.WARNING(
                        f"  > ACCIÓN: Borrar ContentMaterial ID {duplicate_material.id} del Subject duplicado."
                    ))
                    if not dry_run:
                        duplicate_material.delete()
                    deleted_count += 1

                elif not master_material and duplicate_material:
                    self.stdout.write(self.style.WARNING(
                        f"  > ACCIÓN: Reasignar ContentMaterial ID {duplicate_material.id} al Subject maestro."
                    ))
                    if not dry_run:
                        duplicate_material.subjects.add(master_subject)
                        duplicate_material.subjects.remove(duplicate_subject)
                    reassigned_count += 1
        
        end_time = time.time()
        self.stdout.write(self.style.SUCCESS(f"\n{mode} Proceso completado."))
        self.stdout.write(f"  > Asignaturas candidatas analizadas: {processed_count}")
        self.stdout.write(f"  > Contenidos duplicados borrados: {deleted_count}")
        self.stdout.write(f"  > Contenidos huérfanos reasignados: {reassigned_count}")
        self.stdout.write(f"  > Tiempo total: {end_time - start_time:.2f} segundos.")

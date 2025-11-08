# /home/MiguelAeTxio/CampuStudiOnline/academic_structure/management/commands/calculate_content_hashes.py
from django.core.management.base import BaseCommand
from django.db.models import Q
from academic_structure.models import Subject, ContentHashFamily
from django.db import transaction
import time

class Command(BaseCommand):
    help = 'Calcula el hash de contenido de las asignaturas y las asigna a una ContentHashFamily.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            "Iniciando el proceso de cálculo de hashes y asignación a Familias de Contenido..."
        ))
        start_time = time.time()

        # Seleccionar asignaturas con contenido que aún no pertenecen a una familia.
        subjects_to_process = Subject.objects.filter(
            Q(learning_objectives__isnull=False) | 
            Q(course_content_outline__isnull=False) | 
            Q(bibliography__isnull=False)
        ).filter(
            content_hash_family__isnull=True
        ).iterator()

        total_subjects = Subject.objects.filter(
             Q(learning_objectives__isnull=False) | 
             Q(course_content_outline__isnull=False) | 
             Q(bibliography__isnull=False)
        ).filter(content_hash_family__isnull=True).count()
        
        if total_subjects == 0:
            self.stdout.write(self.style.SUCCESS("No hay asignaturas pendientes de procesar. Proceso finalizado."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Asignaturas elegibles encontradas: {total_subjects}"))

        processed_count = 0
        new_families_created = 0
        
        # Caché en memoria para minimizar consultas a la BBDD
        hash_to_family_cache = {}

        for subject in subjects_to_process:
            try:
                calculated_hash = subject._calculate_content_hash()
                
                # Revisa la caché primero
                family = hash_to_family_cache.get(calculated_hash)

                if not family:
                    # Si no está en caché, búscalo o créalo en la BBDD
                    family, created = ContentHashFamily.objects.get_or_create(
                        hash=calculated_hash
                    )
                    if created:
                        new_families_created += 1
                    # Guarda la familia en la caché para futuras iteraciones
                    hash_to_family_cache[calculated_hash] = family

                # Asigna la familia a la asignatura y guarda
                subject.content_hash_family = family
                subject.save(update_fields=['content_hash_family', 'updated_at'])
                
                processed_count += 1
                
                if processed_count % 100 == 0:
                    elapsed_time = time.time() - start_time
                    self.stdout.write(self.style.WARNING(
                        f"  Procesadas {processed_count}/{total_subjects} asignaturas. "
                        f"Tiempo: {elapsed_time:.2f}s"
                    ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error al procesar la asignatura ID {subject.id}: {e}"
                ))
        
        end_time = time.time()
        self.stdout.write(self.style.SUCCESS(
            f"\nProceso completado. "
            f"Total de asignaturas procesadas: {processed_count}. "
            f"Nuevas familias de contenido creadas: {new_families_created}. "
            f"Tiempo total: {end_time - start_time:.2f} segundos."
        ))

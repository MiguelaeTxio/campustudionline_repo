# /home/MiguelAeTxio/CampuStudiOnline/academic_structure/management/commands/detect_hidden_duplicates.py
from django.core.management.base import BaseCommand
from django.db.models import Q
from academic_structure.models import Subject
import time

class Command(BaseCommand):
    help = 'Detecta "duplicados ocultos": asignaturas sin hash cuyo contenido coincide con una asignatura que sí lo tiene.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando detección de duplicados ocultos..."))
        start_time = time.time()

        # 1. Construir un mapa de los hashes que ya existen en la BBDD
        self.stdout.write("Construyendo mapa de hashes maestros...")
        master_hashes = {
            s.content_hash: s.id 
            for s in Subject.objects.filter(content_hash__isnull=False).only('id', 'content_hash')
        }
        self.stdout.write(self.style.SUCCESS(f"Mapa construido con {len(master_hashes)} hashes únicos."))

        # 2. Obtener los candidatos a ser duplicados ocultos
        # (aquellos con contenido pero sin hash)
        hidden_duplicate_candidates = Subject.objects.filter(
            Q(learning_objectives__isnull=False) | Q(course_content_outline__isnull=False) | Q(bibliography__isnull=False),
            content_hash__isnull=True
        )
        
        total_candidates = hidden_duplicate_candidates.count()
        if total_candidates == 0:
            self.stdout.write(self.style.SUCCESS("No se encontraron candidatos a duplicados ocultos. Proceso finalizado."))
            return
            
        self.stdout.write(self.style.NOTICE(f"Analizando {total_candidates} candidatos..."))
        
        found_duplicates_count = 0
        
        # 3. Iterar sobre los candidatos y comparar sus hashes calculados en memoria
        for candidate in hidden_duplicate_candidates.iterator():
            try:
                # Calcular el hash en memoria sin guardar
                calculated_hash = candidate._calculate_content_hash()
                
                # Comprobar si este hash ya existe en nuestro mapa maestro
                if calculated_hash in master_hashes:
                    found_duplicates_count += 1
                    master_id = master_hashes[calculated_hash]
                    
                    self.stdout.write(self.style.WARNING("\n--- DUPLICADO OCULTO ENCONTRADO ---"))
                    self.stdout.write(f"  > Asignatura Maestra (con hash): ID={master_id}")
                    self.stdout.write(f"  > Asignatura Duplicada (sin hash): ID={candidate.id} ({candidate.name})")
                    self.stdout.write(f"  > Hash compartido: {calculated_hash[:16]}...")

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error al procesar candidato ID {candidate.id}: {e}"
                ))

        end_time = time.time()
        self.stdout.write(self.style.SUCCESS(
            f"\nProceso completado. Total de duplicados ocultos encontrados: {found_duplicates_count}. "
            f"Tiempo total: {end_time - start_time:.2f} segundos."
        ))



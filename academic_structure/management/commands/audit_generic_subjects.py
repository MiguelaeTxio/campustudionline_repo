from django.core.management.base import BaseCommand
from django.db.models import Q
from academic_structure.models import Subject
import os

class Command(BaseCommand):
    help = 'Audita asignaturas genéricas candidatas a eliminación.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando auditoría de asignaturas genéricas...'))

        # Definir patrones de búsqueda (case-insensitive)
        PATTERNS = {
            'TFG/TFM': ['Trabajo Fin de', 'TFG', 'TFM', 'Trabajo de Fin de'],
            'Prácticas': ['Prácticas', 'Practicum', 'Estancias', 'Rotatorio', 'Prácticas Externas'],
            'Reconocimientos': ['Reconocimiento de', 'Créditos por'],
            'Jornadas/Eventos': ['Jornadas', 'Seminario', 'Conferencias'],
            'Idiomas Genéricos': ['Idioma Moderno', 'Acreditación de Idioma'],
            'Otros': ['Culturales', 'Deportivas', 'Solidarias']
        }

        # Diccionario para almacenar IDs encontrados para evitar duplicados
        found_ids = set()
        
        # Buffer para el reporte
        report_lines = []
        report_lines.append("REPORTE DETALLADO DE ASIGNATURAS GENÉRICAS")
        report_lines.append("==========================================")

        for category, terms in PATTERNS.items():
            query = Q()
            for term in terms:
                query |= Q(name__icontains=term)
            
            subjects = Subject.objects.filter(query).select_related(
                'academic_year__degree__branch__university'
            )
            count = subjects.count()
            
            if count > 0:
                header = f'\n--- Categoría: {category} ({count} encontradas) ---'
                self.stdout.write(self.style.SUCCESS(header))
                report_lines.append(header)
                
                # Mostrar una muestra en consola y guardar todos en el reporte
                for i, s in enumerate(subjects):
                    # Determinar el código de la universidad de forma segura
                    uni_code = 'N/A'
                    if s.academic_year:
                        try:
                            uni_code = s.academic_year.degree.branch.university.code
                        except AttributeError:
                            uni_code = 'ERR_STRUCT'
                    
                    line = f"[{s.subject_type}] {s.name} | {uni_code}"
                    
                    # Consola: solo los primeros 10
                    if i < 10:
                        status = "[DUPLICADO]" if s.id in found_ids else ""
                        self.stdout.write(f"  - {line} {status}")
                    
                    # Reporte: todos
                    if s.id not in found_ids:
                        report_lines.append(line)
                        found_ids.add(s.id)
                
                if count > 10:
                    self.stdout.write(f"  ... y {count - 10} más.")

        total_flagged = len(found_ids)
        summary = f'\n\nTOTAL DE ASIGNATURAS ÚNICAS DETECTADAS: {total_flagged}'
        self.stdout.write(self.style.SUCCESS(summary))
        report_lines.append(summary)
        
        # Generar archivo de reporte en SWAP (Script S)
        report_path = '/home/MiguelAeTxio/SWAP/generic_subjects_report.txt'
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            self.stdout.write(self.style.WARNING(f"Reporte completo generado en: {report_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error escribiendo reporte: {e}"))


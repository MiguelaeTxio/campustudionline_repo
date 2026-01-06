import json
import os
import hashlib
from django.core.management.base import BaseCommand
from django.db import transaction
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject, ContentHashFamily
from academic_structure.utils import normalize_json_for_hash

class Command(BaseCommand):
    help = 'Importa datos procesados de la UMA desde un JSON, gestionando familias de contenido por hash.'

    # Mapeo manual basado en la auditoría de centros
    UMA_CENTERS = {
        '315': 'Escuela de Ingenierías Industriales',
        '314': 'Escuela Técnica Superior de Arquitectura',
        '307': 'Escuela Técnica Superior de Ingeniería de Telecomunicación',
        '306': 'Escuela Técnica Superior de Ingeniería Informática',
        '313': 'Facultad de Bellas Artes',
        '303': 'Facultad de Ciencias',
        '309': 'Facultad de Ciencias de la Comunicación',
        '310': 'Facultad de Ciencias de la Educación',
        '405': 'Facultad de Ciencias de la Salud',
        '301': 'Facultad de Ciencias Económicas y Empresariales',
        '305': 'Facultad de Derecho',
        '312': 'Facultad de Estudios Sociales y del Trabajo',
        '304': 'Facultad de Filosofía y Letras',
        '401': 'Facultad de Marketing y Gestión',
        '302': 'Facultad de Medicina',
        '311': 'Facultad de Psicología y Logopedia',
        '406': 'Facultad de Turismo'
    }

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON ready-to-deploy')

    def calculate_hash(self, objectives, outline, bibliography):
        """Replica la lógica del modelo para encontrar familias existentes."""
        data = {
            'objectives': objectives,
            'outline': outline,
            'bibliography': bibliography,
        }
        normalized_data = normalize_json_for_hash(data)
        return hashlib.sha256(normalized_data.encode('utf-8')).hexdigest()

    def handle(self, *args, **options):
        file_path = options['json_file']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Archivo no encontrado: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(self.style.NOTICE(f"Iniciando importación de {len(data)} registros..."))

        # 1. Universidad (Identidad actualizada)
        uma, _ = University.objects.update_or_create(
            code='UMA',
            defaults={'name': 'Institución Académica de Málaga'}
        )

        stats = {'created': 0, 'updated': 0, 'skipped': 0, 'families': 0}

        for item in data:
            if item.get('extraction_status') != 'READY':
                stats['skipped'] += 1
                continue

            try:
                with transaction.atomic():
                    # 2. Branch (Centro)
                    branch_name = self.UMA_CENTERS.get(item['center_id'], f"Centro UMA {item['center_id']}")
                    branch, _ = Branch.objects.get_or_create(
                        university=uma,
                        name=branch_name
                    )

                    # 3. Degree
                    degree, _ = Degree.objects.get_or_create(
                        branch=branch,
                        code=item['degree_id'],
                        defaults={
                            'name': item['degree'],
                            'degree_type': Degree.DegreeType.BACHELOR
                        }
                    )

                    # 4. Academic Year
                    year_val = int(item['year']) if item['year'] else 0
                    academic_year, _ = AcademicYear.objects.get_or_create(
                        degree=degree,
                        year=year_val
                    )

                    # 5. Gestionar Hash y Familia de Contenido
                    content_hash = self.calculate_hash(
                        item['learning_objectives'],
                        item['course_content_outline'],
                        item['bibliography']
                    )

                    family, created_fam = ContentHashFamily.objects.get_or_create(hash=content_hash)
                    if created_fam:
                        stats['families'] += 1

                    # 6. Subject
                    subject, created = Subject.objects.update_or_create(
                        academic_year=academic_year,
                        name=item['name'],
                        defaults={
                            'content_hash_family': family,
                            'subject_type': Subject.SubjectType.MANDATORY,
                            'learning_objectives': item['learning_objectives'],
                            'course_content_outline': item['course_content_outline'],
                            'bibliography': item['bibliography'],
                        }
                    )

                    if created:
                        stats['created'] += 1
                    else:
                        stats['updated'] += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error procesando {item['name']}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"IMPORTACIÓN FINALIZADA:\n"
            f"- Asignaturas creadas: {stats['created']}\n"
            f"- Asignaturas actualizadas: {stats['updated']}\n"
            f"- Registros sin contenido (omitidos): {stats['skipped']}\n"
            f"- Nuevas Familias de Contenido (Unicidad): {stats['families']}"
        ))


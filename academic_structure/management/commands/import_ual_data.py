import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject

class Command(BaseCommand):
    help = 'Importa datos académicos enriquecidos de la UAL (incluyendo temarios y objetivos).'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta absoluta al archivo JSON.')

    def handle(self, *args, **options):
        json_file_path = options['json_file']

        if not os.path.exists(json_file_path):
            raise CommandError(f'El archivo {json_file_path} no existe.')

        self.stdout.write(self.style.WARNING(f'Leyendo datos enriquecidos de {json_file_path}...'))

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        try:
            with transaction.atomic():
                # 1. Universidad
                uni, _ = University.objects.get_or_create(
                    code=data['code'],
                    defaults={'name': data['name']}
                )
                self.stdout.write(f"Universidad: {uni.name}")

                # 2. Ramas
                for branch_name, degrees_list in data.get('branches', {}).items():
                    branch, _ = Branch.objects.get_or_create(university=uni, name=branch_name)
                    
                    # 3. Grados
                    for deg_data in degrees_list:
                        degree, _ = Degree.objects.get_or_create(
                            branch=branch,
                            name=deg_data['name'],
                            defaults={
                                'code': deg_data['code'],
                                'degree_type': Degree.DegreeType.BACHELOR
                            }
                        )

                        # 4. Asignaturas
                        subjects_updated = 0
                        for subj_data in deg_data.get('subjects', []):
                            academic_year, _ = AcademicYear.objects.get_or_create(
                                degree=degree,
                                year=subj_data['year']
                            )

                            # Actualizamos o creamos con los datos ricos
                            subject, created = Subject.objects.update_or_create(
                                academic_year=academic_year,
                                name=subj_data['name'],
                                semester=subj_data['semester'],
                                defaults={
                                    'subject_type': subj_data.get('type', 'OT'),
                                    'learning_objectives': subj_data.get('learning_objectives', []),
                                    'course_content_outline': subj_data.get('course_content_outline', []),
                                    'bibliography': subj_data.get('bibliography', {})
                                }
                            )
                            subjects_updated += 1
                        
                        # Feedback reducido para no saturar consola
                        if subjects_updated > 0:
                            self.stdout.write(f"  -> {degree.name}: {subjects_updated} asignaturas procesadas.")

        except Exception as e:
            raise CommandError(f'Error importando datos: {e}')

        self.stdout.write(self.style.SUCCESS('IMPORTACIÓN DE DATOS ENRIQUECIDOS COMPLETADA.'))

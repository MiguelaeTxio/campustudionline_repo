import json
import os
import hashlib
import re
from django.core.management.base import BaseCommand
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject
from django.db import transaction

class Command(BaseCommand):
    help = 'Importación Final UMA: Limpieza de nombres, Hashing y Estructura correcta'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON')

    def handle(self, *args, **options):
        json_path = options['json_file']
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'Falta archivo: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(self.style.SUCCESS(f'Importando {len(data)} registros...'))

        # 1. Institución
        uma, _ = University.objects.get_or_create(
            code="UMA",
            defaults={'name': "Institución Académica de Málaga", 'url': "https://www.uma.es"}
        )

        # 2. Configuración de Limpieza
        BLACKLIST = [
            'trabajo fin', 'tfg', 'tfm', 'prácticas', 'practicum', 
            'visitas', 'reconocimiento', 'estancia', 'movilidad', 'rotatorio'
        ]

        BRANCH_MAP = {
            'Medicina': 'Ciencias de la Salud', 'Salud': 'Ciencias de la Salud',
            'Ingenier': 'Ingeniería y Arquitectura', 'Informática': 'Ingeniería y Arquitectura',
            'Ciencias': 'Ciencias', 'Filosofía': 'Artes y Humanidades',
            'Económicas': 'Ciencias Sociales y Jurídicas', 'Derecho': 'Ciencias Sociales y Jurídicas'
        }

        def get_branch(name):
            for k, v in BRANCH_MAP.items():
                if k.lower() in name.lower(): return v
            return "Ciencias Sociales y Jurídicas"

        def clean_degree_title(name):
            # Quita "Graduado/a en " y "Plan 20XX"
            name = name.replace("Graduado/a en ", "")
            name = re.sub(r'\.?\s*Plan\s*\d{4}', '', name, flags=re.IGNORECASE)
            return name.strip()

        count_created = 0
        
        with transaction.atomic():
            for item in data:
                try:
                    name_raw = item.get('name', '').strip()
                    
                    # Filtro Anti-Ruido
                    if any(bad in name_raw.lower() for bad in BLACKLIST):
                        continue

                    # Rama
                    branch_name = get_branch(item.get('center', ''))
                    branch, _ = Branch.objects.get_or_create(university=uma, name=branch_name)

                    # Grado (Limpieza + Hash)
                    raw_degree = item.get('degree', '')
                    degree_clean = clean_degree_title(raw_degree)
                    
                    # Hash único para el código (10 chars)
                    degree_code = f"UMA-{hashlib.md5(degree_clean.encode()).hexdigest()[:6].upper()}"
                    
                    degree, _ = Degree.objects.get_or_create(
                        branch=branch,
                        name=degree_clean,
                        defaults={'code': degree_code}
                    )

                    # Año (Usamos el dato real extraído por tu algoritmo)
                    year_num = int(item.get('academic_year', 1))
                    academic_year, _ = AcademicYear.objects.get_or_create(
                        degree=degree, 
                        year=year_num
                    )

                    # Asignatura
                    clean_subject_name = name_raw.split("(")[0].strip()
                    
                    subject, created = Subject.objects.get_or_create(
                        academic_year=academic_year,
                        name=clean_subject_name,
                        defaults={'subject_type': Subject.SubjectType.MANDATORY, 'semester': 1}
                    )

                    # Contenido
                    if item.get('status') == 'SUCCESS':
                        subject.learning_objectives = item.get('learning_objectives', [])
                        subject.course_content_outline = item.get('course_content_outline', [])
                        subject.bibliography = item.get('bibliography', {})
                        subject.save()

                    if created: count_created += 1

                except Exception as e:
                    print(f"Skip {item.get('name')}: {e}")

        self.stdout.write(self.style.SUCCESS(f'FIN: {count_created} asignaturas importadas correctamente.'))

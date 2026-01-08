import json
import os
import hashlib
import re
from collections import defaultdict
from django.core.management.base import BaseCommand
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject
from django.db import transaction

class Command(BaseCommand):
    help = 'Importación UMA: Filtro de Planes, URL IDs y Limpieza Avanzada'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON')

    def handle(self, *args, **options):
        json_path = options['json_file']
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'Falta archivo: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(self.style.SUCCESS(f'Analizando {len(data)} registros...'))

        # --- LÓGICA DE FILTRADO DE PLANES ---
        # 1. Agrupar planes por Titulación Base
        # Ejemplo: "Grado en Derecho" -> [2010, 2020]
        degree_plans = defaultdict(list)
        
        def parse_degree_name(raw_name):
            # Extrae "Grado en X" y el año del plan
            # Formato esperado: "Graduado/a en X. Plan YYYY"
            match = re.search(r'(.*?)\.?\s*Plan\s*(\d{4})', raw_name, re.IGNORECASE)
            if match:
                base_name = match.group(1).replace("Graduado/a en ", "").strip()
                year = int(match.group(2))
                return base_name, year
            return raw_name.replace("Graduado/a en ", "").strip(), 0

        # Primer pase para detectar el plan máximo
        for item in data:
            d_name = item.get('degree', '')
            base, year = parse_degree_name(d_name)
            if year > 0:
                degree_plans[base].append(year)

        # Determinar el plan ganador para cada carrera
        winning_plans = {k: max(v) for k, v in degree_plans.items() if v}
        
        self.stdout.write(f"- Planes analizados: Se conservarán solo las versiones más recientes.")

        # --- CONFIGURACIÓN DE FILTROS ---
        BLACKLIST = [
            'trabajo fin', 'tfg', 'tfm', 'prácticas', 'practicum', 
            'visitas', 'reconocimiento', 'estancia', 'movilidad', 'rotatorio',
            'tutorías', 'coordinación', 'laboratorio', 'laboratorios'
        ]
        
        # Palabras que, si están presentes, SALVAN el registro aunque parezca sospechoso
        # (Aunque en este caso 'Trabajo Social' no contiene 'trabajo fin', es bueno prevenir)
        WHITELIST = ['trabajo social']

        BRANCH_MAP = {
            'medicina': 'Ciencias de la Salud', 'salud': 'Ciencias de la Salud', 'enfermería': 'Ciencias de la Salud',
            'psicología': 'Ciencias de la Salud', 'fisioterapia': 'Ciencias de la Salud', 'logopedia': 'Ciencias de la Salud',
            'ingenier': 'Ingeniería y Arquitectura', 'informática': 'Ingeniería y Arquitectura', 'arquitectura': 'Ingeniería y Arquitectura',
            'telecomunic': 'Ingeniería y Arquitectura', 'industri': 'Ingeniería y Arquitectura', 'politéc': 'Ingeniería y Arquitectura',
            'ciencias': 'Ciencias', 'biología': 'Ciencias', 'química': 'Ciencias', 'matemáticas': 'Ciencias',
            'filosofía': 'Artes y Humanidades', 'letras': 'Artes y Humanidades', 'historia': 'Artes y Humanidades',
            'arte': 'Artes y Humanidades', 'traducción': 'Artes y Humanidades', 'filología': 'Artes y Humanidades',
            'económicas': 'Ciencias Sociales y Jurídicas', 'derecho': 'Ciencias Sociales y Jurídicas',
            'sociales': 'Ciencias Sociales y Jurídicas', 'comercio': 'Ciencias Sociales y Jurídicas',
            'educación': 'Ciencias Sociales y Jurídicas', 'turismo': 'Ciencias Sociales y Jurídicas',
            'comunicación': 'Ciencias Sociales y Jurídicas', 'periodismo': 'Ciencias Sociales y Jurídicas'
        }

        def get_branch(center_name):
            c_lower = center_name.lower()
            for k, v in BRANCH_MAP.items():
                if k in c_lower: return v
            return "Ciencias Sociales y Jurídicas"

        def extract_year_from_url_id(url, code_backup):
            # Intenta sacar ID de URL: ...P3_ID:171740-5258-101
            # El último bloque es el código de asignatura
            code = code_backup
            match = re.search(r'P3_ID:[\d-]+-(\d+)', url or '')
            if match:
                code = match.group(1)
            
            code_str = str(code).strip()
            
            # Lógica 3 dígitos: 101 -> 1, 405 -> 4
            if code_str.isdigit() and len(code_str) == 3:
                century = int(code_str[0])
                if 1 <= century <= 6:
                    return century
            return 0 # Fallback

        # --- EJECUCIÓN ---
        uma, _ = University.objects.get_or_create(
            code="UMA",
            defaults={'name': "Institución Académica de Málaga", 'url': "https://www.uma.es"}
        )

        count_created = 0
        count_skipped_plan = 0
        count_skipped_black = 0

        with transaction.atomic():
            for item in data:
                try:
                    name_raw = item.get('name', '').strip()
                    name_lower = name_raw.lower()
                    
                    # 1. Filtro Whitelist/Blacklist
                    is_safe = any(w in name_lower for w in WHITELIST)
                    if not is_safe:
                        if any(bad in name_lower for bad in BLACKLIST):
                            count_skipped_black += 1
                            continue

                    # 2. Filtro de Plan
                    d_raw = item.get('degree', '')
                    d_base, d_year = parse_degree_name(d_raw)
                    
                    # Si la carrera tiene planes registrados y este año no es el ganador, SKIP
                    if d_year > 0 and d_base in winning_plans:
                        if d_year < winning_plans[d_base]:
                            count_skipped_plan += 1
                            continue

                    # Rama
                    branch_name = get_branch(item.get('center', ''))
                    branch, _ = Branch.objects.get_or_create(university=uma, name=branch_name)

                    # Grado
                    degree_code = f"UMA-{hashlib.md5(d_base.encode()).hexdigest()[:6].upper()}"
                    degree, _ = Degree.objects.get_or_create(
                        branch=branch,
                        name=d_base, # Usamos el nombre limpio sin "Plan XXXX"
                        defaults={'code': degree_code}
                    )

                    # Año (Lógica URL)
                    real_year = extract_year_from_url_id(item.get('url_source'), item.get('code'))
                    if real_year == 0:
                        real_year = int(item.get('academic_year', 1))

                    academic_year, _ = AcademicYear.objects.get_or_create(
                        degree=degree, 
                        year=real_year
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
                    print(f"Error en {item.get('name')}: {e}")

        self.stdout.write(self.style.SUCCESS(f'IMPORTACIÓN COMPLETADA.'))
        self.stdout.write(f'- Insertados/Actualizados: {count_created}')
        self.stdout.write(f'- Omitidos por Plan Antiguo: {count_skipped_plan}')
        self.stdout.write(f'- Omitidos por Blacklist: {count_skipped_black}')


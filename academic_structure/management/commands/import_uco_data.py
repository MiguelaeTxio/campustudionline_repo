import json
import os
import hashlib
import unicodedata
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject, ContentHashFamily

class Command(BaseCommand):
    help = 'Ingesta UCO con Mapeo Oficial de Ramas (Opción C - Investigada)'

    # Diccionario Maestro: Nombre del Grado (normalizado) -> Rama Oficial UCO
    # Fuente: Portal de Transparencia UCO / Junta de Andalucía
    OFFICIAL_MAPPING = {
        # ARTES Y HUMANIDADES
        'cine y cultura': 'Artes y Humanidades',
        'estudios ingleses': 'Artes y Humanidades',
        'filologia hispanica': 'Artes y Humanidades',
        'gestion cultural': 'Artes y Humanidades',
        'historia': 'Artes y Humanidades',
        'historia del arte': 'Artes y Humanidades',
        'traduccion e interpretacion': 'Artes y Humanidades',
        
        # CIENCIAS
        'biologia': 'Ciencias',
        'bioquimica': 'Ciencias',
        'ciencias ambientales': 'Ciencias',
        'fisica': 'Ciencias',
        'quimica': 'Ciencias',
        'ciencia y tecnologia de los alimentos': 'Ciencias', # Adscripción oficial UCO
        'enologia': 'Ciencias', # Adscripción oficial UCO
        
        # CIENCIAS DE LA SALUD
        'enfermeria': 'Ciencias de la Salud',
        'fisioterapia': 'Ciencias de la Salud',
        'medicina': 'Ciencias de la Salud',
        'veterinaria': 'Ciencias de la Salud',
        'psicologia': 'Ciencias de la Salud',
        
        # CIENCIAS SOCIALES Y JURÍDICAS
        'administracion y direccion de empresas': 'Ciencias Sociales y Jurídicas',
        'derecho': 'Ciencias Sociales y Jurídicas',
        'educacion infantil': 'Ciencias Sociales y Jurídicas',
        'educacion primaria': 'Ciencias Sociales y Jurídicas',
        'educacion social': 'Ciencias Sociales y Jurídicas',
        'relaciones laborales y recursos humanos': 'Ciencias Sociales y Jurídicas',
        'turismo': 'Ciencias Sociales y Jurídicas',
        'doble grado en derecho y administracion y direccion de empresas': 'Ciencias Sociales y Jurídicas',
        
        # INGENIERÍA Y ARQUITECTURA
        'ingenieria agroalimentaria y del medio rural': 'Ingeniería y Arquitectura',
        'ingenieria civil': 'Ingeniería y Arquitectura', # Belmez
        'ingenieria de la energia y recursos minerales': 'Ingeniería y Arquitectura', # Belmez
        'ingenieria electrica': 'Ingeniería y Arquitectura',
        'ingenieria electronica industrial': 'Ingeniería y Arquitectura',
        'ingenieria forestal': 'Ingeniería y Arquitectura',
        'ingenieria informatica': 'Ingeniería y Arquitectura',
        'ingenieria mecanica': 'Ingeniería y Arquitectura'
    }

    def normalize_name(self, input_str):
        if not input_str: return ""
        # Eliminar "Grado en " si existe
        clean = input_str.lower().replace('grado en ', '').strip()
        # Normalizar acentos
        nfkd_form = unicodedata.normalize('NFKD', clean)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def get_official_branch(self, degree_name):
        norm_name = self.normalize_name(degree_name)
        
        # 1. Búsqueda Exacta en Diccionario Oficial
        if norm_name in self.OFFICIAL_MAPPING:
            return self.OFFICIAL_MAPPING[norm_name]
            
        # 2. Búsqueda Aproximada (si hay ligeras variaciones en el nombre)
        for key, branch in self.OFFICIAL_MAPPING.items():
            if key == norm_name or (len(key) > 5 and key in norm_name):
                return branch

        # 3. Fallback Heurístico (Red de Seguridad)
        if any(x in norm_name for x in ['ingenieria', 'informatica', 'civil', 'minas', 'electrica']):
            return 'Ingeniería y Arquitectura'
        if any(x in norm_name for x in ['arte', 'historia', 'filologia', 'humanidades']):
            return 'Artes y Humanidades'
        if any(x in norm_name for x in ['salud', 'medicina', 'enfermeria']):
            return 'Ciencias de la Salud'
        if any(x in norm_name for x in ['quimica', 'fisica', 'biologia']):
            return 'Ciencias'
            
        return 'Ciencias Sociales y Jurídicas' # Default final

    def handle(self, *args, **options):
        json_path = os.path.join(settings.BASE_DIR, 'web_scrapping', 'uco_final_data_enriched.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'No se encuentra: {json_path}'))
            return

        self.stdout.write(f"Iniciando ingesta UCO (Mapeo Oficial V20)...")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 1. Institución
        university, _ = University.objects.get_or_create(
            code="UCO",
            defaults={
                "name": "Institución Académica de Córdoba",
                "url": "https://www.uco.es"
            }
        )
        if university.name != "Institución Académica de Córdoba":
            university.name = "Institución Académica de Córdoba"
            university.save()

        # 2. Crear las 5 Ramas Estándar
        branch_names = sorted(list(set(self.OFFICIAL_MAPPING.values())))
        branches_cache = {}
        for b_name in branch_names:
            branch, _ = Branch.objects.get_or_create(university=university, name=b_name)
            branches_cache[b_name] = branch

        with transaction.atomic():
            stats = {'degrees': 0, 'years': 0, 'subjects': 0, 'hashes': 0}
            processed_degrees = {} 
            
            for item in data:
                degree_name = item.get('degree')
                year_num = item.get('year')
                subj_name = item.get('name')
                raw_text = item.get('raw_text', '') or ''
                
                if not degree_name or not subj_name: continue

                try: year_num = int(year_num)
                except: continue

                # Gestión Grado
                if degree_name not in processed_degrees:
                    existing = Degree.objects.filter(branch__university=university, name=degree_name).first()
                    if existing:
                        processed_degrees[degree_name] = existing
                    else:
                        branch_name = self.get_official_branch(degree_name)
                        target_branch = branches_cache[branch_name]
                        
                        deg_hash = hashlib.md5(degree_name.encode()).hexdigest()[:4].upper()
                        new_degree = Degree.objects.create(
                            branch=target_branch,
                            name=degree_name,
                            code=f"UCO-{deg_hash}",
                            degree_type=Degree.DegreeType.BACHELOR
                        )
                        processed_degrees[degree_name] = new_degree
                        stats['degrees'] += 1
                        self.stdout.write(f"  [NUEVO] {degree_name} -> {branch_name}")

                degree = processed_degrees[degree_name]

                # Año
                academic_year, created = AcademicYear.objects.get_or_create(degree=degree, year=year_num)
                if created: stats['years'] += 1

                # Hash Family
                content_source = raw_text if len(raw_text) > 100 else f"{degree_name}-{subj_name}-{year_num}"
                content_hash = hashlib.sha256(content_source.encode('utf-8')).hexdigest()
                hash_family, created = ContentHashFamily.objects.get_or_create(hash=content_hash)
                if created: stats['hashes'] += 1

                # Asignatura
                subject, created = Subject.objects.update_or_create(
                    academic_year=academic_year,
                    name=subj_name,
                    semester=None,
                    defaults={
                        "subject_type": Subject.SubjectType.MANDATORY,
                        "content_hash_family": hash_family,
                        "course_content_outline": [raw_text[:8000]] if raw_text else []
                    }
                )
                if created: stats['subjects'] += 1

                if stats['subjects'] % 500 == 0:
                    self.stdout.write(f"   ... {stats['subjects']} items procesados.")

            self.stdout.write(self.style.SUCCESS(f"""
            --- RESUMEN FINAL ---
            Grados: {stats['degrees']}
            Asignaturas: {stats['subjects']}
            Familias Hash: {stats['hashes']}
            """))

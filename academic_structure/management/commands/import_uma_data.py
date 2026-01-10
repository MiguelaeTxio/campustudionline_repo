import json
import os
import hashlib
import re
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject
from orchestrator.models import PendingContentTask

class Command(BaseCommand):
    help = 'Importación UMA: Ingesta de datos limpios desde uma_data_final.json'

    def add_arguments(self, parser):
        parser.add_argument(
            "--purge",
            action="store_true",
            help="Elimina TODAS las universidades y datos asociados antes de importar. ¡PRECAUCIÓN!",
        )

    def handle(self, *args, **options):
        # --- PURGA DE SEGURIDAD ---
        if options["purge"]:
            self.stdout.write(self.style.WARNING("Modo --purge activado. Eliminando datos académicos existentes..."))
            self.stdout.write(self.style.WARNING("-> Eliminando tareas pendientes de contenido..."))
            PendingContentTask.objects.all().delete()
            
            # Buscamos específicamente la UMA
            uma_qs = University.objects.filter(code="UMA")
            if uma_qs.exists():
                uma_obj = uma_qs.first()
                self.stdout.write(f"-> Iniciando borrado manual escalonado para {uma_obj.name}...")
                
                # 1. Borrar Asignaturas (Romper vínculo más fuerte)
                subjs_count, _ = Subject.objects.filter(academic_year__degree__branch__university=uma_obj).delete()
                self.stdout.write(f"   - Asignaturas borradas: {subjs_count}")
                
                # 2. Borrar Años
                years_count, _ = AcademicYear.objects.filter(degree__branch__university=uma_obj).delete()
                self.stdout.write(f"   - Años borrados: {years_count}")
                
                # 3. Borrar Grados
                degrees_count, _ = Degree.objects.filter(branch__university=uma_obj).delete()
                self.stdout.write(f"   - Grados borrados: {degrees_count}")
                
                # 4. Borrar Ramas
                branches_count, _ = Branch.objects.filter(university=uma_obj).delete()
                self.stdout.write(f"   - Ramas borradas: {branches_count}")
                
                # 5. Borrar Universidad
                uma_obj.delete()
                self.stdout.write(self.style.SUCCESS("-> Universidad UMA eliminada correctamente."))
            else:
                self.stdout.write("-> No se encontró la universidad UMA para purgar.")

        # --- CARGA DEL JSON ---
        # Ruta canónica según estructura del proyecto
        json_file_path = "data/uma_data_final.json"

        if not os.path.exists(json_file_path):
             # Fallback para pruebas locales si no está en la ruta relativa
            if os.path.exists("/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/data/uma_data_final.json"):
                json_file_path = "/home/MiguelAeTxio/PROJECTS/CampuStudiOnline/data/uma_data_final.json"
            else:
                raise CommandError(f"No se encuentra el archivo de datos: {json_file_path}")

        self.stdout.write(self.style.NOTICE(f"--- Iniciando importación UMA desde: {json_file_path} ---"))

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(self.style.SUCCESS(f'Analizando {len(data)} registros...'))

        # --- LÓGICA DE DETECCIÓN DE PLANES (WINNING PLAN) ---
        # Agrupamos por nombre base para quedarnos solo con el plan más reciente
        degree_plans = defaultdict(list)
        
        def parse_degree_name(raw_name):
            # "Graduado/a en Derecho. Plan 2010" -> ("Derecho", 2010)
            clean = raw_name.replace("Graduado/a en ", "").strip()
            match = re.search(r'(.*?)\.?\s*Plan\s*(\d{4})', clean, re.IGNORECASE)
            if match:
                base_name = match.group(1).strip()
                year = int(match.group(2))
                return base_name, year
            return clean, 0

        # Barrido para encontrar años máximos
        for item in data:
            d_name = item.get('degree', '')
            base, year = parse_degree_name(d_name)
            if year > 0:
                degree_plans[base].append(year)

        winning_plans = {k: max(v) for k, v in degree_plans.items() if v}
        self.stdout.write(f"- Filtro de planes: Se han identificado {len(winning_plans)} titulaciones con versiones múltiples.")

        # --- MAPEO DE RAMAS (Inferido por Facultad) ---
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
            return "Ciencias Sociales y Jurídicas" # Default

        # --- EJECUCIÓN ---
        stats = {
            'uni_created': 0, 'branch_created': 0, 'degree_created': 0, 
            'subject_created': 0, 'subject_updated': 0,
            'skipped_plan': 0
        }

        try:
            with transaction.atomic():
                # 1. Universidad
                uma, created = University.objects.get_or_create(
                    code="UMA",
                    defaults={'name': "Institución Académica de Málaga", 'url': "https://www.uma.es"}
                )
                if created: stats['uni_created'] += 1

                # 2. Iteración de Registros
                for item in data:
                    try:
                        # -- Filtro de Plan --
                        d_raw = item.get('degree', '')
                        d_base, d_year = parse_degree_name(d_raw)
                        
                        if d_year > 0 and d_base in winning_plans:
                            if d_year < winning_plans[d_base]:
                                stats['skipped_plan'] += 1
                                continue

                        # -- Rama --
                        branch_name = get_branch(item.get('center', ''))
                        branch, created = Branch.objects.get_or_create(university=uma, name=branch_name)
                        if created: stats['branch_created'] += 1

                        # -- Grado --
                        # Generamos un código único basado en el nombre base limpio
                        degree_code = f"UMA-{hashlib.md5(d_base.encode()).hexdigest()[:8].upper()}"
                        
                        degree, created = Degree.objects.get_or_create(
                            branch=branch,
                            name=d_base,
                            defaults={
                                'code': degree_code,
                                'degree_type': Degree.DegreeType.BACHELOR # Asumimos Grado por defecto
                            }
                        )
                        if created: stats['degree_created'] += 1

                        # -- Año Académico --
                        # Usamos el dato limpio del scraping, asegurando int
                        try:
                            year_val = int(item.get('academic_year', 1))
                        except:
                            year_val = 1
                            
                        academic_year, _ = AcademicYear.objects.get_or_create(
                            degree=degree, 
                            year=year_val
                        )

                        # -- Asignatura --
                        name_raw = item.get('name', '').strip()
                        # Limpieza final de nombre (quitar paréntesis si los hay al final tipo "(Semipresencial)")
                        clean_name = name_raw.split("(")[0].strip()

                        defaults_dict = {
                            'subject_type': Subject.SubjectType.MANDATORY, # Default seguro
                            'semester': 1, # Default seguro, UMA no siempre lo da
                            'learning_objectives': item.get('learning_objectives', []),
                            'course_content_outline': item.get('course_content_outline', []),
                            'bibliography': item.get('bibliography', {})
                        }


                        if not academic_year or not academic_year.pk:
                            self.stderr.write(f"CRITICAL: AcademicYear inválido para {clean_name}")
                            continue

                        subject, created = Subject.objects.update_or_create(
                            academic_year=academic_year,
                            name=clean_name,
                            defaults=defaults_dict
                        )

                        if created:
                            stats['subject_created'] += 1
                        else:
                            stats['subject_updated'] += 1

                    except Exception as e:
                        self.stderr.write(f"Error procesando registro {item.get('name')}: {e}")

        except Exception as e:
            raise CommandError(f"Error fatal en transacción: {e}")

        self.stdout.write(self.style.SUCCESS('\nIMPORTACIÓN UMA FINALIZADA.'))
        self.stdout.write(f"- Ramas creadas: {stats['branch_created']}")
        self.stdout.write(f"- Grados creados: {stats['degree_created']}")
        self.stdout.write(f"- Asignaturas creadas: {stats['subject_created']}")
        self.stdout.write(f"- Asignaturas actualizadas: {stats['subject_updated']}")
        self.stdout.write(self.style.WARNING(f"- Registros omitidos por Plan Antiguo: {stats['skipped_plan']}"))

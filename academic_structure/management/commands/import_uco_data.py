import json
import re
import sys
from django.core.management.base import BaseCommand
from academic_structure.models import University, Branch, Degree, Subject, AcademicYear
from orchestrator.models import PendingContentTask, ContentRequest

class Command(BaseCommand):
    help = "Importador V9: Purga manual por niveles para evitar errores de integridad."

    def add_arguments(self, parser):
        parser.add_argument("--purge", action="store_true", help="Eliminar datos previos.")

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(">>> EJECUTANDO IMPORTADOR V9 <<<"))
        
        json_file = "data/uco_data_final.json"
        uco_code = "UCO"

        if options["purge"]:
            self.stdout.write("Iniciando purga manual por niveles...")
            try:
                # 1. Eliminar dependencias en Orchestrator
                PendingContentTask.objects.filter(subject__academic_year__degree__branch__university__code=uco_code).delete()
                ContentRequest.objects.filter(subject__academic_year__degree__branch__university__code=uco_code).delete()
                
                # 2. Eliminar Asignaturas directamente (Hijos)
                subjs_del, _ = Subject.objects.filter(academic_year__degree__branch__university__code=uco_code).delete()
                self.stdout.write(f"- Asignaturas eliminadas: {subjs_del}")

                # 3. Eliminar Años Académicos
                years_del, _ = AcademicYear.objects.filter(degree__branch__university__code=uco_code).delete()
                self.stdout.write(f"- Años eliminados: {years_del}")

                # 4. Eliminar el resto de la estructura
                University.objects.filter(code=uco_code).delete()
                self.stdout.write(self.style.SUCCESS("Purga manual finalizada."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Aviso: La purga automatizada falló ({e}), se intentará importar sobre datos existentes."))

        # CARGA JSON
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error crítico leyendo JSON: {e}"))
            return

        uni, _ = University.objects.get_or_create(
            code=uco_code,
            defaults={"name": "Universidad de Córdoba", "url": "https://www.uco.es"}
        )
        
        subject_type_map = {
            "troncal": Subject.SubjectType.CORE,
            "obligatoria": Subject.SubjectType.MANDATORY,
            "optativa": Subject.SubjectType.OPTIONAL,
            "formación básica": Subject.SubjectType.BASIC
        }

        count_ok, count_err, total = 0, 0, len(data)
        self.stdout.write(f"Iniciando importación de {total} registros...")

        for i, item in enumerate(data):
            try:
                branch_name = item.get('branch', 'General').strip()
                degree_name = item.get('degree', 'Grado Desconocido').strip()
                subject_name = item.get('name', 'Asignatura Desconocida').strip()
                try: year_num = int(item.get('year', 1))
                except: year_num = 1
                
                clean_degree = re.sub(r'[^A-Z0-9]', '', degree_name.upper())[:15]
                degree_code = f"UCO-{clean_degree}"

                # Obtención de objetos con verificación de persistencia
                branch, _ = Branch.objects.get_or_create(university=uni, name=branch_name)
                degree, _ = Degree.objects.get_or_create(
                    branch=branch, name=degree_name, defaults={"code": degree_code}
                )
                academic_year, _ = AcademicYear.objects.get_or_create(degree=degree, year=year_num)

                raw_type = item.get('subject_type', 'Obligatoria').lower()
                db_type = subject_type_map.get(raw_type, Subject.SubjectType.OTHER)
                if db_type == "OT" and "básica" in raw_type: db_type = "BA"

                Subject.objects.update_or_create(
                    academic_year=academic_year,
                    name=subject_name[:255],
                    semester=None,
                    defaults={
                        "subject_type": db_type,
                        "learning_objectives": item.get('learning_objectives', []),
                        "course_content_outline": item.get('course_content_outline', []),
                        "bibliography": item.get('bibliography', {})
                    }
                )
                count_ok += 1
            except Exception as e:
                count_err += 1
                if count_err < 10: # No saturar el log si hay muchos errores
                    self.stdout.write(self.style.ERROR(f"Error en {subject_name}: {e}"))
            
            if i % 200 == 0:
                sys.stdout.write(f"\rProgreso: {i}/{total} | OK: {count_ok} | ERR: {count_err}")
                sys.stdout.flush()

        self.stdout.write(self.style.SUCCESS(f"\nPROCESO COMPLETADO. OK: {count_ok} | ERR: {count_err}"))

# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/academic_structure/management/commands/import_us_data.py
import json
import re
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from academic_structure.models import University, Branch, Degree, Subject, AcademicYear

class Command(BaseCommand):
    """
    Management command to import data for 'Institución Académica de Sevilla'.
    Uses RUCT mapping logic to assign degrees to correct branches.
    """
    help = "Importa datos de la Institución Académica de Sevilla desde us_dataset_FINAL.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--purge",
            action="store_true",
            help="Borra los datos previos de la Institución de Sevilla antes de importar.",
        )

    def get_branch_name(self, degree_name):
        """Mapeador RUCT basado en la adscripción oficial de la US."""
        dn = degree_name.lower()
        
        # 1. CIENCIAS DE LA SALUD
        if any(x in dn for x in ["enfermería", "fisioterapia", "medicina", "odontología", "podología", "psicología", "biomedicina", "óptica", "optometría", "salud"]):
            return "Ciencias de la Salud"
        
        # 2. INGENIERÍA Y ARQUITECTURA
        if any(x in dn for x in ["ingeniería", "arquitectura", "edificación", "aeroespacial", "computadores", "software"]):
            return "Ingeniería y Arquitectura"
        
        # 3. CIENCIAS
        if any(x in dn for x in ["biología", "bioquímica", "estadística", "física", "matemáticas", "química"]) and "ingeniería" not in dn:
            return "Ciencias"
        
        # 4. ARTES Y HUMANIDADES
        if any(x in dn for x in ["bellas artes", "conservación", "restauración", "árabes", "asia oriental", "franceses", "ingleses", "filología", "filosofía", "historia", "lengua", "literatura", "arqueología", "alemán"]):
            return "Artes y Humanidades"
        
        # 5. CIENCIAS SOCIALES Y JURÍDICAS
        return "Ciencias Sociales y Jurídicas"

    def handle(self, *args, **options):
        json_file_path = "data/PHASE_2_WEST/us_dataset_FINAL.json"
        
        if options["purge"]:
            self.stdout.write(self.style.WARNING("--- Iniciando purga selectiva de la Institución de Sevilla ---"))
            # Eliminamos solo lo relacionado con esta institución para no afectar a UGR/UMA
            University.objects.filter(code="USEV").delete()
            self.stdout.write(self.style.SUCCESS("Purga de 'USEV' completada."))

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            raise CommandError(f"Error al leer el archivo JSON: {e}")

        stats = {"branches": 0, "degrees": 0, "subjects": 0}

        # Mapa de tipos de asignatura según el modelo Subject
        type_map = {
            "formación básica": Subject.SubjectType.BASIC,
            "obligatoria": Subject.SubjectType.MANDATORY,
            "optativa": Subject.SubjectType.OPTIONAL,
            "troncal": Subject.SubjectType.CORE,
        }

        try:
            with transaction.atomic():
                # 1. Sincronización de la Universidad (Marca Institucional)
                uni_obj, _ = University.objects.update_or_create(
                    code="USEV",
                    defaults={
                        "name": "Institución Académica de Sevilla",
                        "url": "https://www.us.es",
                    },
                )

                for degree_data in data.get("data", []):
                    degree_name = degree_data.get("degree_name")
                    branch_label = self.get_branch_name(degree_name)

                    # 2. Sincronización de la Rama
                    branch_obj, created = Branch.objects.get_or_create(
                        university=uni_obj,
                        name=branch_label
                    )
                    if created: stats["branches"] += 1

                    # 3. Sincronización del Grado
                    # Generamos un código corto basado en el nombre
                    clean_name = re.sub(r'[^A-Z0-9]', '', degree_name.upper())
                    degree_code = f"US-{clean_name[:15]}"
                    
                    degree_obj, created = Degree.objects.update_or_create(
                        branch=branch_obj,
                        name=degree_name,
                        defaults={
                            "code": degree_code,
                            "degree_type": Degree.DegreeType.MASTER if "máster" in degree_name.lower() else Degree.DegreeType.BACHELOR,
                            "url": degree_data.get("degree_url"),
                        },
                    )
                    if created: stats["degrees"] += 1

                    # 4. Sincronización de Asignaturas
                    for sub_data in degree_data.get("subjects", []):
                        # Academic Year (Curso)
                        try:
                            year_val = int(sub_data.get("course", 1))
                        except (ValueError, TypeError):
                            year_val = 1
                            
                        ay_obj, _ = AcademicYear.objects.get_or_create(
                            degree=degree_obj,
                            year=year_val
                        )

                        # Tipo de asignatura
                        raw_type = sub_data.get("type", "").lower()
                        s_type = type_map.get(raw_type, Subject.SubjectType.OTHER)
                        
                        # Asignatura
                        Subject.objects.update_or_create(
                            academic_year=ay_obj,
                            name=sub_data.get("name", "").strip(),
                            defaults={
                                "subject_type": s_type,
                                "learning_objectives": sub_data.get("learning_objectives", []),
                                "course_content_outline": sub_data.get("course_content_outline", []),
                            }
                        )
                        stats["subjects"] += 1

            self.stdout.write(self.style.SUCCESS(
                f"\nPROCESO COMPLETADO:\n"
                f" - Ramas creadas/detectadas: {stats['branches']}\n"
                f" - Grados importados: {stats['degrees']}\n"
                f" - Asignaturas enriquecidas: {stats['subjects']}"
            ))

        except Exception as e:
            raise CommandError(f"Fallo crítico en la transacción: {e}")

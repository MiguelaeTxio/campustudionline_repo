# /home/MiguelAeTxio/PROJECTS/CampuStudiOnline/academic_structure/management/commands/import_uja_data.py
import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from academic_structure.models import University, Branch, Degree, AcademicYear, Subject

class Command(BaseCommand):
    help = 'Importa datos UJA con lógica de actualización (MOVER asignaturas de curso).'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON limpio')

    def handle(self, *args, **options):
        json_path = options['json_file']
        
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f'Archivo no encontrado: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(f"Iniciando importación INTELIGENTE de {len(data)} titulaciones...")

        with transaction.atomic():
            uni, _ = University.objects.get_or_create(
                code="UJA",
                defaults={"name": "Institución Académica de Jaén", "url": "https://www.ujaen.es"}
            )

            updated_count = 0
            moved_count = 0

            for degree_data in data:
                # Titulación
                branch_name = degree_data.get('branch_name', 'Sin Rama')
                branch, _ = Branch.objects.get_or_create(university=uni, name=branch_name)
                
                degree, _ = Degree.objects.get_or_create(
                    branch=branch,
                    name=degree_data['degree_name'],
                    defaults={"code": degree_data.get('degree_code', ''), "degree_type": "GR"}
                )

                # Mapa de Años para acceso rápido
                year_objs = {}
                for y in range(1, 6): # Hasta 5 o 6 años
                    ay, _ = AcademicYear.objects.get_or_create(degree=degree, year=y)
                    year_objs[y] = ay

                subjects_list = degree_data.get('subjects', [])
                
                for subj in subjects_list:
                    s_name = subj['name']
                    target_year_num = subj.get('year', 1)
                    target_ay = year_objs.get(target_year_num, year_objs[1])

                    # 1. BUSCAR ASIGNATURA EXISTENTE (Por nombre y titulación, IGNORANDO AÑO)
                    # Esto es clave para detectar la "zombie" en Año 1 y moverla.
                    existing_subj = Subject.objects.filter(
                        academic_year__degree=degree,
                        name=s_name
                    ).first()

                    if existing_subj:
                        # Si existe, verificar si está en el año correcto
                        if existing_subj.academic_year != target_ay:
                            old_year = existing_subj.academic_year.year
                            existing_subj.academic_year = target_ay
                            existing_subj.save()
                            moved_count += 1
                            # self.stdout.write(f"  ↪️ Movida: {s_name} (Año {old_year} -> {target_year_num})")
                        else:
                            # Ya está bien
                            pass
                    else:
                        # Crear nueva
                        Subject.objects.create(
                            academic_year=target_ay,
                            name=s_name,
                            subject_type="OB", # Default
                            semester=subj.get('semester')
                        )
                        updated_count += 1

            self.stdout.write(self.style.SUCCESS(f"PROCESO FINALIZADO."))
            self.stdout.write(f" - Asignaturas nuevas creadas: {updated_count}")
            self.stdout.write(f" - Asignaturas MOVIDAS de curso: {moved_count}")
